from pygame import mixer
import cv2
import time
import mediapipe as mp

mixer.init()

songs = [
     r"C:\Users\marah\Downloads\Radiohead - Creep.mp3",
     r"c:\Users\marah\Downloads\Tame Impala - Let It Happen (Official Audio).mp3",
     r"c:\Users\marah\Downloads\Kanye West - Bound 2 (audio)-trim.mp3"
]

song_index = 0
mixer.music.load(songs[song_index])

mixer.music.play()
mixer.music.pause()
#Mediapipe

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands =1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

#camera
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

playing = False

last_action_time = 0
cooldown = 1 

volume = 0.5
mixer.music.set_volume(volume)

while True:
    success, img = cam.read()

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    #if there are hands

    if results.multi_hand_landmarks:

        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            #position of the tip of the index finger
        
            lm = handLms.landmark

            thumb = lm[4].y
            index_finger = lm [8].y
            middle_finger = lm[12].y

            #if the tip of the index finger is above the tip of the thumb, play the music
            
            hand_open = abs(thumb - index_finger) > 0.1
            current_time = time.time()

            if hand_open and not playing:

                    mixer.music.unpause()
                    playing = True
                    print("PLAY")  

            elif not hand_open and playing:

                    mixer.music.pause()
                    playing =False
                    print("STOP")


           # ✌️ إصبعين = NEXT SONG
            if (
             index_finger < lm[6].y and
             middle_finger < lm[10].y
            ):

                 if current_time - last_action_time > cooldown:

                    song_index += 1

                    if song_index >= len(songs):
                        song_index = 0

                    mixer.music.load(songs[song_index])
                    mixer.music.play()

                    playing = True
                    last_action_time = current_time

                    print("NEXT SONG")


    # ☝️ إصبع واحد = PREVIOUS SONG
            if (
                index_finger < lm[6].y and
                middle_finger > lm[10].y
            ):

                if current_time - last_action_time > cooldown:

                    song_index -= 1

                    if song_index < 0:
                        song_index = len(songs) - 1

                    mixer.music.load(songs[song_index])
                    mixer.music.play()

                    playing = True
                    last_action_time = current_time

                    print("PREVIOUS SONG") 
            
            distance = abs(thumb - index_finger)
            volume = max(0.2, min(1.0, 1 - distance))
            mixer.music.set_volume(volume)

    cv2.imshow("Air music controller", img)

    if cv2.waitKey(1) == 27:
        break

cam.release()
cv2.destroyAllWindows()
