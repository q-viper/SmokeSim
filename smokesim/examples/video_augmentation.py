
import cv2
import mediapipe as mp
from smokesim.augmentation import Augmentation
import numpy as np
import pygame
from pathlib import Path

if __name__ == "__main__":
    np.random.seed(100)

    RUN_LIVE = False
    WIDTH, HEIGHT = 700, 500

    video_path = Path("media/vid.mp4")
    augmentation = Augmentation(image_path=None, screen_dim=(WIDTH, HEIGHT))

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    if RUN_LIVE:
        cap = cv2.VideoCapture(0)
    else:
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found at {video_path}")
        cap = cv2.VideoCapture(str(video_path))
    fno = 0
    with mp_hands.Hands(
        max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as hands:
        while True:
            fno += 1
            ret, frame = cap.read()
            x, y = None, None
            if ret:
                frame = np.fliplr(frame).astype(np.uint8)
                screen_frame = cv2.resize(
                    cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE),
                    augmentation.image.get_size()[::-1],
                )
                image_rgb = cv2.cvtColor(screen_frame, cv2.COLOR_BGR2RGB)
                results = hands.process(image_rgb)

                # Draw hand landmarks on the image.
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            screen_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                        )
                        index_finger_tip = hand_landmarks.landmark[
                            mp_hands.HandLandmark.INDEX_FINGER_TIP
                        ]
                        h, w, _ = image_rgb.shape
                        x = int(index_finger_tip.x * w)
                        y = int(index_finger_tip.y * h)

                        cv2.circle(screen_frame, (x, y), 10, (0, 255, 0), -1)

                augmentation.screen.blit(
                    pygame.surfarray.make_surface(screen_frame),
                    (0, 0),
                )
                if fno % 2 == 0:
                    augmentation.add_smoke(
                        dict(
                            color=augmentation.smoke_machine.color,
                            particle_count=5,
                            origin=(
                                (
                                    np.random.randint(100, WIDTH),
                                    np.random.randint(100, HEIGHT),
                                )
                                if (x, y) == (None, None)
                                else (y, x)
                            ),
                            lifetime=5000,
                            particle_args={
                                "min_lifetime": 500,
                                "max_lifetime": 1000,
                                "min_scale": 10,
                                "max_scale": 50,
                                "fade_speed": 1,
                                "scale": 25,
                                "smoke_sprite_size": 25,
                                "color": augmentation.smoke_machine.color,
                            },
                        )
                    )
                # print(augmentation.clock.tick(30))
                augmentation.augment(30)
                rgb_array = pygame.surfarray.array3d(pygame.display.get_surface())

                aframe = cv2.rotate(rgb_array, cv2.ROTATE_90_CLOCKWISE)
                frame = cv2.resize(frame, (aframe.shape[1], aframe.shape[0]))

                cv2.imshow("frame", frame)
                cv2.imshow("aframe", aframe)

            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()
    cv2.destroyAllWindows()
    augmentation.end()