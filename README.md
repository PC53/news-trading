
# News Trading Application 

![Screenshot 2024-05-25 152209](https://github.com/PC53/news-trading/assets/56227421/84998288-ad9d-44fe-beea-1628522a0935)


## Project Structure

```
my_trading_app/
│
├── frontend/       # ReactJS frontend
├── backend/        # Flask application
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
└── scraper/        # Scraper and scheduler
    ├── scraper.py
    ├── Dockerfile
    └── requirements.txt
```

## Prerequisites

- Docker
- Docker Compose

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/my_trading_app.git
   cd my_trading_app
   ```

2. **Build and run the Docker containers:**

   ```bash
   docker-compose up --build
   ```

## Environment Variables

The following environment variables are used in the project:

- **MONGO_URI**: MongoDB connection URI
- **JWT_SECRET_KEY**: Secret key for JWT token generation

Set these variables in your environment or in the `docker-compose.yml` file.

## Contributing

Feel free to open issues or submit pull requests if you find any bugs or have suggestions for improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

