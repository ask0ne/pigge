# pigge

## Please maintain the project structure

The main project files are inside pigge folder. This is to keep deployment and development files seperate.
Each feature has been given it's own folder and each feature has it's own templates. For the time being, all the static files i.e css, js and images and same.

So for example, auth contains all the login/registraion logic and files related to it.


├───migrations (DB stuff)
│
└───pigge
    │   config.py               (Flask configuration)
    │   main.py                 (Where the magic happens)
    │   models.py               (DB models)
    │
    ├───auth
    │   │   auth.py             (Login and registraion view)
    │   │   registration.py     (Login and registration logic)
    │   │
    │   └───templates           (Login and registration HTML files)
    │
    ├───kdash
    │   │   kdash.py            (Kid dashboard code will go here)
    │   │
    │   └───templates           (* HTML files)
    │
    ├───pdash
    │   │   pdash.py            (Parent dashboard)
    │   │   session.py          (Session for parent login)
    │   │
    │   └───templates
    │
    ├───static
    │   ├───css                 (All .css files)
    │   ├───images              (Images here)
    │   └───js                  (JS here)
    │
    ├───templates               (index.html)
    │
    └───uploads                 (Student ID card will be stored here)