# Real-Time Event Booking System

A modern event booking platform built with Django and Tailwind CSS, featuring real-time notifications, payment integration, and an advanced admin panel.

## Features

- Calendar-based booking system
- Real-time notifications using WebSockets
- Stripe payment integration
- Dark theme with modern UI
- Advanced admin dashboard
- User management system
- Email notifications
- Responsive design

## Tech Stack

- Django 4.2
- Channels (WebSockets)
- Tailwind CSS
- Redis
- Celery
- Stripe
- PostgreSQL

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Tailwind CSS dependencies:
```bash
python manage.py tailwind install
```

4. Set up environment variables:
Create a .env file in the root directory with:
```
SECRET_KEY=your_secret_key
DEBUG=True
STRIPE_PUBLIC_KEY=your_stripe_public_key
STRIPE_SECRET_KEY=your_stripe_secret_key
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Start the development server:
```bash
python manage.py runserver
```

8. In a separate terminal, start Tailwind CSS build process:
```bash
python manage.py tailwind start
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
# event_booking
