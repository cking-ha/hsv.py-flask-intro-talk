UNIX Pipes as a Service (UPaaS) slides and code
-----------------------------------------------

Here's a short list of instructions to quickly deploy this code:

1. Obtain a (free) [heroku account](https://signup.heroku.com/)
2. Install the heroku command locally (instructions [here](https://devcenter.heroku.com/articles/heroku-cli))
3. cd to the root of this project, and run `heroku login && heroku create`; follow the prompts to login when requested
4. Add a (free) rabbitMQ instance: `heroku addons:create rabbitmq-bigwig:pipkin`
5. Push the code up to heroku to deploy: `git push heroku master`
6. Open the code in a browser: `heroku open`

Heroku, by default, will give you several hundered hours per month of free testing time. Make changes, commit them to git, and push to the heroku remote in order to make changes.

Happy hacking!
