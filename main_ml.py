from video_redactor.ml_controller import MLController
import ray


if __name__ == "__main__":
    controller = MLController()
    controller.process_ml()
    ray.shutdown()
