import { useEffect, useRef } from "react";
import { FaceDetection } from "@mediapipe/face_detection";
import { Camera } from "@mediapipe/camera_utils";

export default function EyeContactTracker({ onScore }) {
  const videoRef = useRef(null);
  let detectedFrames = 0;
  let totalFrames = 0;

  useEffect(() => {
    const faceDetection = new FaceDetection({
      locateFile: (file) =>
        `https://cdn.jsdelivr.net/npm/@mediapipe/face_detection/${file}`,
    });

    faceDetection.setOptions({
      model: "short",
      minDetectionConfidence: 0.5,
    });

    faceDetection.onResults((results) => {
      totalFrames++;
      if (results.detections && results.detections.length > 0) {
        detectedFrames++;
      }
    });

    const camera = new Camera(videoRef.current, {
      onFrame: async () => {
        await faceDetection.send({ image: videoRef.current });
      },
      width: 320,
      height: 240,
    });

    camera.start();

    return () => {
      camera.stop();
      const score = Math.round(
        (detectedFrames / Math.max(totalFrames, 1)) * 10
      );
      onScore(score);
    };
  }, []);

  return (
    <video
      ref={videoRef}
      autoPlay
      muted
      style={{ display: "none" }}
    />
  );
}
