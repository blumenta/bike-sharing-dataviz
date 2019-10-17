# bike-sharing-dataviz
A minimalistic dashboard for visualizing bike sharing data from the JCDecaux API.

![gif](imgs/bike-viz-demo.gif)

## Requirements
To run the web app locally you'll need 
* your own API key for accessing the 
live data from [JCDecaux](https://developer.jcdecaux.com/#/home).
* an anaconda python installation

## Install
* Create a file called `api_key.json` in the root of the project with the following content 
`{"key": "your_JCDecaux_api_key"}`.
* Install dependencies: `conda env create -f environment.yml`

## Serve
To serve the app just run
*  `conda activate bike-dataviz` to activate the environment.
* `panel serve main.py` to run the web app
* connect to `localhost:5006/main` in a web browser
