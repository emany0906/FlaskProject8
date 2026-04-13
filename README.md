Flag Viewer - IS2209 Group Project
Group: Robert Higgins (124440812), Emanuel Youssef (124453644), Tim Twohig (124467104)
GitHub Repository: https://github.com/emany0906/FlaskProject8
Live Application: https://flaskproject8.onrender.com
About
Flag Viewer is a Flask web application that lets users browse country flags from around the world, save their favourite ones, and delete saved flags. It integrates with a Supabase PostgreSQL database for storage and the FlagCDN API for flag images.
Setup and Running Locally

Clone the repository:
git clone https://github.com/emany0906/FlaskProject8
Install dependencies:
pip install -r requirements.txt
Create a .env file in the root folder (see .env.example for the required variables):
DATABASE_URL=your_database_url_here
Run the application:
python -m flask run
Open your browser and go to:
http://127.0.0.1:5000

Running with Docker

Build the image:
docker build -t flagviewer .
Run the container:
docker run -p 5000:5000 --env-file .env flagviewer
Open your browser and go to:
http://127.0.0.1:5000

Environment Variables
DATABASE_URL - PostgreSQL connection string (Supabase)
API Endpoints
GET / - Main UI
GET /get_flag/n - Get flag by index
GET /get_random_flag - Get a random flag
POST /save_flag - Save a flag to the database
GET /get_saved_flags - Get all saved flags
DELETE /delete_flag - Delete a saved flag by country code
CI/CD Overview
The project uses GitHub Actions for continuous integration and deployment. On every pull request the pipeline runs linting and tests and builds the Docker image. On merge to main the Docker image is published to GitHub Container Registry and the application is automatically deployed to Render.
External Sources
Flag images and country codes provided by FlagCDN (https://flagcdn.com)