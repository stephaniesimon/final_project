# show+tell

show+tell is an interactive audio journal built by <a href="http://linkedin.com/in/stephsimon" target="_blank">Stephanie Simon</a>. Send a request to your grandmother to record her coveted family recipes, generate and edit the transcripts, and create a recipe book instantly.

<img src="/static/images/readme/readme_hp.png" alt="show+tell homepage">

#### Technology Stack

d3, JavaScript, jQuery, HTML, CSS, Bootstrap, Python, Flask, Jinja, SQLAlchemy, SQLite, Amazon Web Services - S3 Buckets, boto 

#### APIs

<a href="https://github.com/mattdiamond/Recorderjs" target="_blank">Recorder.js</a>, <a href="https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API" target="_blank">HTML5 Web Audio</a>

#### Background

Voice is an especially powerful and intimate way to communicate personality. 

show+tell marries my interest in storytelling, podcasts, database work and front end technologies to create an interactive audio journal. A visually-compelling way to record, remember and share who you are, via voice.

#### Overview

The user registers or logs in (and can play with a cool Force Layout d3 vis).

Interesting personality questions are shown for the user to answer - sourced from Proust and various other sources. The user can skip through them until finding one they'd like to make a recording for.

<img src="/static/images/readme/readme_profile.png" alt="show+tell profile">

On the web interface, show+tell uses the **Recorder.js** and **HTML5 Web Audio APIs** to capture audio recordings. 

After the audio file is created, the blob is sent to the server and converted into a WAV file. It's given a file name and stored in an **Amazon S3 bucket**.

When the user is ready to view their visualization, a in-memory csv file is created using **StringIO** and used by the **d3.csv** function to render the user's visualization.

<img src="/static/images/readme/readme_vis.png" alt="show+tell vis">

Recorded answers are represented by nodes. Nodes are color-coded by question category (legend displayed beneath vis) and their size is correlated to the size of the audio file (larger node = longer recording). 

The music button toggles background music to create a more immersive experience, and the Tweet button enables sharing.

