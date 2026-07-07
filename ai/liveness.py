import numpy as np

class LivenessDetector:
    def __init__(self, ear_threshold=0.21, consecutive_frames=2):
        self.ear_threshold = ear_threshold
        self.consecutive_frames = consecutive_frames
        self.blink_counter = 0
        self.total_blinks = 0
        self.prev_nose_pos = None
        self.movement_detected = False

    @staticmethod
    def euclidean_dist(p1, p2):
        return np.linalg.norm(np.array(p1) - np.array(p2))

    def calculate_ear(self, eye_points):
        # Compute vertical distances between eye landmarks
        a = self.euclidean_dist(eye_points[1], eye_points[5])
        b = self.euclidean_dist(eye_points[2], eye_points[4])
        # Compute horizontal distance
        c = self.euclidean_dist(eye_points[0], eye_points[3])
        # Eye Aspect Ratio
        ear = (a + b) / (2.0 * c)
        return ear

    def check_liveness(self, face_landmarks):
        """
        Processes face landmarks for a single frame.
        Returns:
            blink_detected (bool): True if a blink event was resolved
            movement_detected (bool): True if subtle face movement (3D depth change or shifting) is noted
            ear (float): Average EAR for debug/display
        """
        # 1. Blink Detection (EAR)
        left_eye = face_landmarks.get('left_eye')
        right_eye = face_landmarks.get('right_eye')
        
        ear = 0.0
        if left_eye and right_eye:
            left_ear = self.calculate_ear(left_eye)
            right_ear = self.calculate_ear(right_eye)
            ear = (left_ear + right_ear) / 2.0

            if ear < self.ear_threshold:
                self.blink_counter += 1
            else:
                if self.blink_counter >= self.consecutive_frames:
                    self.total_blinks += 1
                    self.blink_counter = 0
                    # Reset blink counter and flag blink detected
                    blink_resolved = True
                else:
                    self.blink_counter = 0
                    blink_resolved = False
        else:
            blink_resolved = False

        # 2. Movement / Texture fluctuation check (using nose bridge / tip)
        nose_bridge = face_landmarks.get('nose_bridge')
        if nose_bridge:
            current_nose_pos = np.array(nose_bridge[3]) # Nose tip approximation
            if self.prev_nose_pos is not None:
                dist = self.euclidean_dist(self.prev_nose_pos, current_nose_pos)
                # If there's slight natural head movement (above threshold but not shaking wildly)
                if 0.5 < dist < 15.0:
                    self.movement_detected = True
            self.prev_nose_pos = current_nose_pos

        return blink_resolved or self.total_blinks > 0, self.movement_detected, ear

    def reset(self):
        self.blink_counter = 0
        self.total_blinks = 0
        self.prev_nose_pos = None
        self.movement_detected = False
