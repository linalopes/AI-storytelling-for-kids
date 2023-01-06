# AI-storytelling-for-kids

During the meeting at [Hackergarden Lucerne](https://www.hackergarten.net/) on 05/01/2023, we created this digital interactive book-experience for kids.

The idea was using a webcam to recognize some drawings on paper and start generating stories using [chatGPT](https://chat.openai.com/chat).

For the input, we used [Teachable Machine](https://teachablemachine.withgoogle.com/) to train our model with a deck of seed drawings. 
Each drawing was converted into 100-200 webcam images capturing different size and orientations. 

After training, we exported our model using [Keras Tensorflow](https://keras.io/).

Check out [AI storytelling for kids](https://aiforkids.maquinada.art/) to create your own story!
