from datetime import datetime, timedelta
from .models import Cita, Especialista


def calculate_available_hours(fecha, especialista_id):
    print(especialista_id)
    appointment_duration = timedelta(hours=1)
    available_hours = []

    # Convert the given fecha string to a datetime object
    fecha_datetime = datetime.strptime(fecha, "%Y-%m-%d")

    # Get the working hours for the especialista
    especialista = Especialista.objects.get(pk=especialista_id)
    working_start_time = datetime(
        fecha_datetime.year, fecha_datetime.month, fecha_datetime.day, 9, 0
    )
    working_end_time = datetime(
        fecha_datetime.year, fecha_datetime.month, fecha_datetime.day, 17, 0
    )

    # Get all citas for the given especialista on the specified fecha
    citas_for_especialista = Cita.objects.filter(
        especialista_id=especialista_id, fecha=fecha
    )

    # Create a set of booked time slots based on existing citas
    booked_time_slots = {cita.hora.strftime("%H:%M") for cita in citas_for_especialista}

    # Loop through the working hours and find available time slots
    current_hour = working_start_time
    while current_hour < working_end_time:
        current_time_str = current_hour.strftime("%H:%M")

        # Check if the current time slot is not booked
        if current_time_str not in booked_time_slots:
            available_hours.append(current_time_str)

        # Increment the current hour by the appointment duration
        current_hour += appointment_duration

    return available_hours
