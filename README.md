# pigge

## Please maintain the project structure

The main project files are inside pigge folder. This is to keep deployment and development files seperate.
Each feature has been given it's own folder and each feature has it's own templates. For the time being, all the static files i.e css, js and images and same.

So for example, auth contains all the login/registraion logic and files related to it.



wallet_id - FOR EXTERNAL USE ONLY AKA USED BY KIDS TO PAY OTHER KIDS

Other IDs are used for INTERNAL PURPOSE ONLY

├───migrations (DB stuff) <br>
│<br>
└───pigge<br>
    │   config.py               (Flask configuration)<br>
    │   main.py                 (Where the magic happens)<br>
    │   models.py               (DB models)<br>
    │<br>
    ├───auth<br>
    │   │   auth.py             (Login and registraion view)<br>
    │   │   registration.py     (Login and registration logic)<br>
    │   │<br>
    │   └───templates           (Login and registration HTML files)<br>
    │<br>
    ├───kdash<br>
    │   │   kdash.py            (Kid dashboard code will go here)<br>
    │   │<br>
    │   └───templates           (* HTML files)<br>
    │
    ├───pdash<br>
    │   │   pdash.py            (Parent dashboard)<br>
    │   │   session.py          (Session for parent login)<br>
    │   │<br>
    │   └───templates<br>
    │<br>
    ├───static<br>
    │   ├───css                 (All .css files)<br>
    │   ├───images              (Images here)<br>
    │   └───js                  (JS here)<br>
    │<br>
    ├───templates               (index.html)<br>
    │<br>
    └───uploads                 (Student ID card will be stored here)<br>