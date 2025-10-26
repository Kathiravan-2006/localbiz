# LocalBiz - Local Business Directory

LocalBiz is a Django-based web application that serves as a directory for local businesses. It allows businesses to create listings, users to search and review businesses, and administrators to manage the platform.

## Features

- Business Listings (CRUD operations)
- Search and filter businesses by name, category, and location
- Rating and review system
- User authentication and profiles
- Admin dashboard for platform management
- Responsive design with custom CSS
- MongoDB backend using Djongo

## Prerequisites

- Python 3.8 or higher
- MongoDB
- pip (Python package manager)

## Usage

### For Business Owners

1. Register an account
2. Log in to your account
3. Click "Add Your Business" to create a new listing
4. Fill in your business details
5. Wait for admin approval
6. Manage your business listing and respond to reviews

### For Customers

1. Browse businesses on the homepage
2. Use the search and filter options to find specific businesses
3. View business details and reviews
4. Create an account to leave reviews
5. Rate businesses and share your experiences

### For Administrators

1. Log in with superuser credentials
2. Access the admin dashboard
3. Approve new business listings
4. Manage users and reviews
5. Monitor platform activity

## Project Structure

```
localbiz/
├── core/                 # Main application
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── forms.py         # Form definitions
│   └── urls.py          # URL patterns
├── templates/           # HTML templates
│   ├── base.html       # Base template
│   ├── home.html       # Homepage
│   └── ...             # Other templates
├── static/             # Static files
│   ├── css/           # CSS styles
│   └── js/            # JavaScript files
└── localbiz/          # Project settings
    ├── settings.py    # Project configuration
    └── urls.py        # Main URL configuration
```

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please email support@localbiz.com or create an issue in the GitHub repository. 
