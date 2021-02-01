# pigge

## TODO

<ol>
<li>Flash messages for errors</li>
<li>Kid dashboard features</li>
<li>Payment module (K2K and K2B)</li>
<li>Tips and quizzes module</li>
<li>UI/UX fixes</li>
</ol>

## Please maintain the project structure

The main project files are inside pigge folder. This is to keep deployment and development files seperate.
Each feature has been given it's own folder and each feature has it's own templates. For the time being, all the static files i.e css, js and images and same.

So for example, auth contains all the login/registraion logic and files related to it.

##### Some important notes
> wallet_id

FOR EXTERNAL USE ONLY AKA USED BY KIDS TO PAY OTHER KIDS

Other IDs are used for INTERNAL PURPOSE ONLY

> session['user_mail'] 

Contains email of current logged in user (parent or kid)

> session['id']

Contains WALLET ID of the kid. So even if the parent is logged in, kid's wallet ID is accessed.

This is fine for now because either way both fields are public and known to the user. Later we have to find a way to secure this or find some other way.

├───migrations<br>
└───pigge<br>
    ├───auth<br>
    │   └───templates<br>
    │       └───auth<br>
    ├───kdash<br>
    │   └───templates<br>
    │       └───kdash<br>
    ├───payment<br>
    │   └───templates<br>
    │       └───payment<br>
    ├───pdash<br>
    │   └───templates<br>
    │       └───pdash<br>
    ├───static<br>
    │   ├───css<br>
    │   ├───images<br>
    │   └───js<br>
    ├───templates<br>
    └───uploads<br>