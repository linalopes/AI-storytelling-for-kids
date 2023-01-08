import random
import openai
import pygame
import pygame.camera
from keras.models import load_model
from PIL import Image, ImageOps  #Install pillow instead of PIL
import numpy as np

recognized_objects = []

def capture_pictures(picture_name):
  input('Press enter to continue to take the picture: ' + picture_name)
  print("Taking picture ....")
  # initializing  the camera
  pygame.camera.init()
    
  # make the list of all available cameras
  camlist = pygame.camera.list_cameras()
    
  # if camera is detected or not
  if camlist:
    # initializing the cam variable with default camera
    cam = pygame.camera.Camera(camlist[0], (1024, 768))
    
    # opening the camera
    cam.start()
    
    # capturing the single image
    image = cam.get_image()
    
    # saving the image
    pygame.image.save(image, picture_name)
    
  # if camera is not detected the moving to else part
  else:
        print("No camera on current device")


def recognize_object(picture_name):
    input('Press enter to recognize object:  ' + picture_name)
    print("Recognizing object ....")
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = load_model('keras_model.h5', compile=False)

    # Load the labels
    class_names = open('labels.txt', 'r').readlines()

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(picture_name).convert('RGB')

    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    #turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    print('Class:', class_name, end='')
    print('Confidence score:', confidence_score)
    recognized_objects.append(class_name)

# for x in range(2):
#   capture_pictures("picture"+str(x))

for x in range(2):
  recognize_object("picture"+str(x))

props = ["Hat", "House", "Car"]
characters = ["Little girl", "Rabbit", "The thing"]
actions = ["blow a house", 
            "hide under the bed",
            "get a shortcut in the forest", 
            "climb a tree", "eat an apple", 
            "write a letter", "play a flute",
            "lose a shoe", "hurt the finger", 
            "kill a dragon"] 

random_action = actions[random.randrange(len(actions)-1)]

prop_to_sentence = ""
character_to_sentence = ""

for prop in props:
    for recognized_object in recognized_objects:
        if recognized_object.find(prop) > -1:
            prop_to_sentence = prop
            print("Object" + prop + "found in recognized objects!")
        else:
            print("NO")

for character in characters:
    for recognized_object in recognized_objects:
        if recognized_object.find(character) > -1:
            character_to_sentence = character
            print("Object" + character + "found in recognized objects!")
        else:
            print("NO")

sentence = "Tell me a short story for kids about a " + prop_to_sentence + " and a " + character_to_sentence + " who " + random_action + "."
print(sentence)

openai.api_key = "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"
# print(openai.Model.list())

response = openai.Completion.create(
  model="text-davinci-003",
  prompt=sentence,
  temperature=0.9,
  max_tokens=2000,
  top_p=1,
  frequency_penalty=0.0,
  presence_penalty=0.6,
  stop=[" Human:", " AI:"]
)

print(response)