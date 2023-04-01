from feature.pipeline import run_feature_pipeline
from intermediate.pipeline import run_intermediate_pipeline
from primary.pipeline import run_primary_pipeline


def run_pipeline():
    run_intermediate_pipeline()
    run_primary_pipeline()
    run_feature_pipeline()


if __name__ == "__main__":
    run_pipeline()
