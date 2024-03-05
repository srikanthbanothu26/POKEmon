Pokémon Management System
This is a web application for managing Pokémon data, allowing users to search for Pokémon, like their favorite ones, and register an account to access additional features.

Features:
Search Pokémon: Users can search for Pokémon by name or ID.
Like Pokémon: Registered users can like their favorite Pokémon.
User Registration: Users can register an account to access additional features.
User Authentication: Registered users can log in to access their account.
Profile Management: Users can manage their profile information and preferences.
Delete Pokémon: Users can delete Pokémon from their collection.
Installation
Clone the repository:
git clone https://github.com/your-username/pokemon-management-system.git
Install dependencies:
cd pokemon-management-system
pip install -r requirements.txt
Set up the database:

Configure your database settings in config.py.
Run the following commands to create and initialize the database:
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
Start the application:
flask run
The application will be running at http://localhost:5000.

Usage
Navigate to the application URL (http://localhost:5000 by default).
Register for a new account or log in with an existing account.
Search for Pokémon using the search feature.
Like your favorite Pokémon by clicking the like button.
Manage your profile and preferences as needed.
Delete Pokémon from your collection if desired.
Contributing
Contributions are welcome! If you have any suggestions or find any issues, please open an issue or submit a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgements
This project was inspired by Pokémon fans and enthusiasts.
Special thanks to Flask for the web framework used in this project.
Pokémon data is sourced from PokéAPI.