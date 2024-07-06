# `Leaf Lounge`
The application is available for viewing [here](https://moment-canvas-68ed5e5eed98.herokuapp.com/).

Also available for viewing here:
[Facebook Page]().

![Leaf Lounge Responsive Image]()
## Introduction
Leaf Lounge is a full-stack Django-framework networking platform, offering book-lovers the unique opportunity to network, share impressions, reviews, and critiques of books. Visitors wishing to join one of Leaf Lounge's vast communities need only register for a Leaf Lounge account, and they immediately gain access to all Leaf Lounge has to offer.

## Table of Contents
- [Business/Social Goals](#businesssocial-goals)
- [UX Goals](#ux-goals)
- [User Stories](#user-stories)
- [Wireframes](#wireframes)
- [Strategy](#strategy)
- [Target Audience](#target-audience)
- [Key Information Deliverables](#key-information-deliverables)
  - [Client Side](#client-side)
  - [Technical](#technical)
  - [Marketing](#marketing)
- [Features](#features)
- [Structure](#structure)
- [Models](#models)
- [Views & Templates](#views--templates)
- [Scope of Application](#scope-of-application)
- [Aesthetics](#aesthetics)
- [Technologies](#technologies)
- [Testing & Debugging](#testing--debugging)
  - [Manual Testing](#manual-testing)
  - [Automated Testing](#automated-testing)
- [Issues](#issues)
- [Accessibility & Performance](#accessibility--performance)
  - [Lighthouse](#lighthouse)
  - [Colour Accessibility Validator](#colour-accessibility-validator)
  - [HTML Validation](#html-validation)
  - [CSS Validation](#css-validation)
  - [JSHint Validation](#jshint-validation)
- [Deployment](#deployment)
  - [Foreword](#foreword)
  - [Step 1: Create an App on Heroku](#step-1-create-an-app-on-heroku)
  - [Step 2: Connect to GitHub](#step-2-connect-to-github)
  - [Step 3: Automatic Deploy (Optional)](#step-3-automatic-deploy-optional)
  - [Step 4: Settings](#step-4-settings)
  - [Step 5: Deploy Your Masterpiece](#step-5-deploy-your-masterpiece)
  - [Step 6: Where is my Application?](#step-6-where-is-my-application)
- [Forking a GitHub Repository](#forking-a-github-repository)
- [Cloning a GitHub Repository](#cloning-a-github-repository)
- [Credits](#credits)
- [Acknowledgements](#acknowledgements)

## Business/Social Goals
- As a first time visitor, I would like to be taken directly to the 'Leaf Lounge' home page so that I have quick access to all relevant information to get started.
- As a site user, I would like a custom profile with my personal information.
- As a site user, I would like the option to read more information on the book before buying it.
- As a site visitor, I require access to the library page so that I can view and choose from available books.
- As a site user, it would be nice to have a contact page so that I could contact the 'Leaf Lounge' team with queries.
- As a site user, I require a checkout page from which I can make secure transactions.
- As a site user, I require access to the chatroom so that I can network with other readers.
- As a site user, I would like the option of viewing the books I have bought and storing them in my profile.
- As a site user, I would like the option of viewing my books before buying them.
- As a site user, I would like the option of amending my books before buying them.
- As a site user, I would like the option of deleting books from my basket.
- As a site user, I require a secure payment system to make transactions.
- As a site user, I require the option of signing-up, signing-in and signing-out of my account.
- As a site visitor, I would like the option of signing up for the Leaf Lounge Newsletter, without needing to register for an account.
- As a site user, I would like access to Leaf Lounge's social media so that I could follow the page and stay up to date.
- As a book lover, I would like the option of putting my old books up for sale or donating them.

## UX Goals
- As a site user, I would like fast access to only the pages that would benefit my experience.
  -  All pages should be displayed based on whether I am registered/logged in.
  - I should be redirected to relevant pages and without coming across site errors.
- As a site user, I would like all pages to follow the same branding guidelines - this includes font family, colours (colour palette), image styles, spacing, and effects. 
- As a site visitor and/or potential reseller, I would like colours to convey the correct emotions to ensure the intended branding message and motives.
- As a site user, I would like all pages to be responsive to ensure I have a good user experience. This includes best practices in legibility, colour contrast, font sizes, branding, and element visibility.

## User Stories
| Id | User Story | Label | User Story Testing |
| ----- | ----- | ----- | ----- |
|  | As a first time visitor, I would like to view the 'moment' home page so that I have quick access to all relevant information to get started. | `must-have` | ----- |
|  | As a site user, I would like access to a custom profile with my personal information and a list of charities I am a part of so that I may view and amend as needed. | `should-have` | ----- |
|  | As a site user, I would like the option to read more information on the charity prior to donating. | `must-have` | ----- |
|  | As a site user, it would be nice to have a contact page so that I could contact the 'Leaf Lounge' team with queries. | `good-to-have` | ----- |
|  | As a site user, I require a donations page from which I can make a secure transaction to the charity of my choosing. | `must-have` | ----- |
|  | As a donatee, I require access to the Charity Canvas to collaborate with other artists. | `must-have` | ----- |
|  | As a donatee, I would like access to a chat room with other people who have donated to the charity for networking and collaboration. | `should-have` | ----- |
|  | As a donatee, I would like the option of viewing my past donations. | `should-have` | ----- |
|  | As a donatee, I would like the option of amending my donations prior to charging my card. | `must-have` | ----- |
|  | As a donatee, I would like the option of deleting items in my basket. | `must-have` | ----- |
|  | As a donatee, I require a secure payment system to make donations to selected charities. | `must-have` | ----- |
|  | As a (potential) donatee, I require the option of signing-up, signing-in and signing-out of my account. | `must-have` | ----- |
|  | As a site visitor, I would like the option of signing up for the Leaf Lounge Newsletter, without needing to register for an account. | `must-have` | ----- |
|  | As a site user/donatee, I would like access to Leaf Lounge's social media so that I could follow the page and stay up to date. | `good-to-have` | ----- |
|  | As a charity organisation, I would like the option of registering my charity so that I could have my own community and raise money for my cause. | `should-have` |  |

## Wireframes
![Leaf Lounge Wireframe](static/images/Leaf Lounge-wireframe.png)

## Strategy
## Target Audience
- Readers
- Book Enthusiasts
- 15+ years of age (payment)
- Publishers

## Key Information Deliverables
For the purposes of navigation, the key information deliverables for this project have been split into three sections, each focusing on a different vital aspect of the project.

#### Client-Side
- _Home page_ with all relevant information about the platform.
- _Checkout page_ with _Stripe_ Payments.
- Community Page
  - _Chatroom_
  - _Reviews_
- Creation of _Personal/Seller Profiles_ for audience expansion.

#### Technical
- _Contact page_ queries reaching Leaf Lounge _Email_.
- _Stripe_ Payments
- Testing files for all app views, urls, and models.

#### Marketing
- [Facebook Page]()
- Clear and intuative branding
- Legibility and responsiveness of all elements on all screen sizing

## Features
## Structure
- Navigation Bar
  - Logo
  - Links
  - Account Management Button

- Home Page*

- Contact Page
  - Contact Form
    - Validation
    - To-Email Queries
    - Success Message

_If user is not signed-in:_
- Create Account (Dropdown button menu)
  - Create Seller
    - Seller Form
    - Success Message
    - Error Message
    - Admin Approval
  - Sign Up/ Sign In (allauth)
    - Sign Up/ Sign In Form
    - Mandatory Email Verification
    - Confirmation Message

_If user is signed in:_
- Manage Account (Dropdown button menu)
  - Create Seller (same functionality)
    - Charity Form
    - Success Message
    - Error Message
    - Admin Approval
  - My Communities*
  - My Payment*
  - Sign Out (allauth)
    - Sign Out Form
    - Confirmation Message

- Footer
  - Links
  - Copyright
    - Dynamic Year

## Models
Below is a simple ERD for `moment`'s models.

![Leaf Lounge ERD]()

#### The xxxxx Model
Fields:

Meta:

#### The xxxxx Model
Fields:

Meta:

## Views & Templates
## Scope of Application
## Aesthetics
## Technologies
1. Django Framework - fullstack technology
2. HTML5/ Django Syntax - Used for structuring and content.
3. CSS3 - Used for adding styles to the content for legibility and aesthetic appeal.
4. Javascript - For adding basic interactivity and dynamically setting URLs.
5. Python - Used for Django manipulation & interaction.
6. FontAwesome/Bootstrap icons - used for icons.
7. Chrome Developer Tools - used for debugging the website during production.
8. Lighthouse - For performance, accessibility, best practices and SEO checking.
9. GitHub - For code storage, version control and deployment.
10. Git - For commiting through the terminal and pushing to GitHub for storage.
11. Gitpod - The IDE I developed the project in.
12. VSC - For quick testing of allauth functionality due to Gitpod's limitations.
12. Balsamiq - For project wireframe design.
13. Color Contrast Accessibility Validator - for checking colour contrast ratios.
14. W3C Markup Validation Service - to validate my HTML for potential errors.
15. W3C CSS Validation Service - to validate my CSS code for potential errors.
16. JSHint - for checking and validating my JS code. 
17. Pep8 - for Python code validation and best practices formatting.

## Testing & Debugging
This section outlines procedures for manual testing. For automated testing, please see all files `test*.py`.

- ## Manual Testing
| Feature | Expected Outcome | Testing Procedure | Result | Remark |
|---|---|---|---|---|

- ## Automated Testing

## Issues
## Accessibility & Performance
### Lighthouse
### Colour Accessibility Validator
### HTML Validation
### CSS Validation
### JSHint Validation

### Pep8 Validation
All python files are regularly validated during development.

## Deployment
The application is deployed on Heroku through Git Hub and is available for viewing in the link at the top of this README.md document. To deploy a Heroku project, please refer to the guide below.

### Foreword
There are some general requirements when it comes to setting up your application and its files: 
- Your dependencies must be placed in the requirements.txt file.
- You must strictly adhere to the correct folder structure expected by Django's settings.
- In Django's settings.py file, setting Debug = True in development will display a detailed errors page if the application comes across an error hindering template rendering. It will also allow the collection of static files (stylesheets, images, and javascript files automatically). Setting Debug = False will display standard error pages under the same conditions and will not update any changes to static files.

In Heroku, this is configured under `Config Vars`, as `COLLECT_STATIC`, with the value of either:
  - `0` for blocking automatic collection
  - `1` for enabling automatic collection.

_Note: Do not commit to GitHub with Debug = True. Always set Debug = False before committing to avoid exposing personal details._

You will need two-factor verification set up to enable log in.

### Step 1: Create an App on Heroku
Log onto your Heroku dashboard using your username and password, and confirm the access code in the two-factor verification app of your choosing.

Create a new Heroku app:
![New Heroku App]()

You will be asked to pick a name and region for your app before clicking `Create app` on the next page.
![New App Options]()

### Step 2: Connect to GitHub
Once you've created your app, go to the `Deploy` tab at the top.

Select the middle box with GitHub's logo to connect your Heroku app to a GitHub Repository.

If prompted, authorize Heroku to access your GitHub account.
At the bottom, enter the name of the repository you wish to deploy to, and click Connect.
![Connect GitHub to Heroku]()

### Step 3: Automatic Deploy (Optional)
Under `Automatic Deploys`, choose a branch from your GitHub repository that Heroku will watch for changes.

Enable automatic deploys by clicking `Enable Automatic Deploys`. With this, every push to the selected branch will automatically deploy a new version of your app.

### Step 4: Settings
When you create the app, you will need to add the `heroku/python` buildpack in the Settings tab. 

### Step 5: Deploy Your Masterpiece
If you've enabled automatic deploys, any push to the selected branch will automatically deploy your application.

If you prefer to deploy manually or want to deploy a branch without enabling automatic deploys, go to `Manual deploy`, select the branch, and click `Deploy Branch`.

### Step 6: Where is my Application?
Your application will have a similar look to the following Heroku URL configuration: (https://*.herokuapp.com) and can be found after clicking the `Open App` button on your dashboard in the top right corner.

![Open App]()

## Forking a GitHub Repository
To make changes to your repository without changing its original state, you can make a copy of it via `fork`. This ensures the original repository remains unchanged. 

Steps:
1. Click into the GitHub repository you want to fork.
2. Click `Fork` in the top right-hand side of the top bar, and this should take you to a page titled `Create a new fork`.
3. You can now work in this copy of your repository without making changes to the original.

## Cloning a GitHub Repository
Cloning a repository essentially means downloading a copy of your repository that can be worked on locally. This method allows for version control and backup of code.

Steps:
1. Click on the GitHub repository you want to clone.
2. Click on the `Code` button.
3. Copy the link in the dropdown.
4. Open a terminal within your VSC (or whatever IDE you choose to use).
5. In the terminal type 'git clone' and paste the URL.
6. Press Enter - you now have a cloned version of your GitHub repository.

## Credits
## Acknowledgements