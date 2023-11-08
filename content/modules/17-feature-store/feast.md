# Feast

Feast is an open-source **feature store** designed to simplify and accelerate the management and serving of ML features. 

It aims to provide a scalable and reliable platform for feature storage, retrieval, and serving, enabling efficient development and deployment of ML models.

!!! info "Info!"
    Feast enables organizations to consistently define, store, and serve ML features and decouple ML from data infrastructure.

## Install `feast`

!!! exercise "Question!"
    Create (or activate) a virtual environment to be used in class.

!!! exercise "Question!"
    After activating the environment, we install `feast` with:

    <p>
    <div class="termy">

    ```console
    $ pip install -U pip
    $ pip install feast
    ```

    </div>
    </p>


## Create folder and Initialize `feast`

Let's create a `feast` project with:

!!! exercise "Question!"
    Make sure you are at the folder you wnat to store this class and run:

    <p>
    <div class="termy">

    ```console
    $ feast init -m experiment
    $ cd experiment/feature_repo
    ```

    </div>
    </p>

!!! exercise "Question!"
    Explore newly created folders and files!

    ```console
    experiment
    ├── feature_repo
    │   ├── feature_store.yaml
    │   └── __init__.py
    └── __init__.py
    ```

!!! exercise "Question!"
    Create a `data` folder at `experiment/feature_repo/data` and paste the `channels.parquet` file there.

    !!! info ""
        The `parquet` file can be found [HERE](https://github.com/Insper/mlops/tree/main/content/modules/17-feature-store/data)!

    Expected tree:

    ```console
    experiment
    ├── feature_repo
    │   ├── data
    │   │   └── channels.parquet
    │   ├── feature_store.yaml
    │   └── __init__.py
    └── __init__.py

    ```

!!! exercise "Question!"
    Create a `notebooks` folder at `experiment/notebooks` and paste the following code just to check `"channels.parquet` file content.

    ```python
    import pandas as pd
    dfc = pd.read_parquet("../feature_repo/data/channels.parquet")
    dfc
    ```


## Configure `feature_store.yaml`

In this file we must configure the data sources. For now we will use data stored locally.

!!! exercise "Question!"
    Change the `experiment/feature_repo/feature_store.yaml` file content to:
    
    ```yaml
    project: exp
    registry: data/registry.db
    provider: local
    online_store:
        type: sqlite
        path: data/online_store.db
    entity_key_serialization_version: 2
    ```

## Define feature repository

!!! exercise "Question!"
    Create a `experiment/feature_repo/define_repo.py` file with the following content.

!!! danger "Important!"
    Change the `path="/full/path/to/experiment/feature_repo/data/channels.parquet"`

    Enter the full path to the parquet file!

??? "Click to see `define_repo.py` source code"

    ```python
    from datetime import timedelta

    import pandas as pd

    from feast import (
        Entity,
        FeatureService,
        FeatureView,
        Field,
        FileSource,
        PushSource,
        RequestSource,
    )
    from feast.on_demand_feature_view import on_demand_feature_view
    from feast.types import Int64, String

    channel = Entity(name="channel", join_keys=["channel_id"])

    channel_stats_source = FileSource(
        name="channel_daily_stats_source",
        path="/path/to/experiment/feature_repo/data/channels.parquet",
        timestamp_field="date",
        created_timestamp_column="created",
    )

    # Here we define a Feature View that will allow us to serve the
    # channel data to our model online.
    channel_stats_fv = FeatureView(
        name="channel_daily_stats",
        entities=[channel],
        ttl=timedelta(days=1),
        # The list of features defined below act as a schema to both define features
        # for both materialization of features into a store, and are used as references
        # during retrieval for building a training dataset or serving features
        schema=[
            Field(name="channel_name", dtype=String),
            Field(name="k_subscribers", dtype=Int64),
            Field(name="30_days_k_views", dtype=Int64, description="Average daily channel stats"),
        ],
        online=True,
        source=channel_stats_source,
        # Tags are user defined key/value pairs that are attached to each
        # feature view
        tags={"team": "youtube_analytics"},
    )
    ```

## Apply changes

!!! exercise "Question!"
    To apply changes, run:

    <p>
    <div class="termy">

    ```console
    $ feast apply
    ```

    </div>
    </p>

## Use features

Let's see how to use the features. To do this, we will query historical data.

!!! exercise "Question!"
    Create a `experiment/get_features.py` file with the following content.

??? "Click to see `get_features.py` source code"

    ```python
    from pprint import pprint
    from feast import FeatureStore
    from datetime import datetime
    import pandas as pd

    store = FeatureStore(repo_path="feature_repo")

    # The keys and filters for the information we want to obtain.
    entity_df = pd.DataFrame.from_dict(
        {
            "channel_id": [1, 1, 5],
            "date": [
                datetime(2023, 11, 7),
                datetime(2023, 11, 6),
                datetime(2023, 11, 7),
            ],
        }
    )

    # The features we want to obtain.
    feature_vector = store.get_historical_features(
        entity_df=entity_df,
        features=[
            "channel_daily_stats:channel_name",
            "channel_daily_stats:k_subscribers",
        ],
    ).to_df()

    pprint(feature_vector)
    ```

!!! exercise "Question!"
    Test by running:

    <p>
    <div class="termy">

    ```console
    $ python get_features.py
    ```

    </div>
    </p>

!!! exercise "Question!"
    Change the code to also return the `channel_daily_stats:30_days_k_views` feature.

    Run it and check if it worked.

!!! exercise text long "Question!"
    Change the code to also return data for the date `2023-11-04` for both channel ids `1` and `5`. What happens?

## User interface

We can also access the **Feast** Web interface. To do this, being in `exp/feature_repo`, run:

<p>
<div class="termy">

```console
$ feast ui
```

</div>
</p>

This was an introduction to **feast**. The tool has many additional features. To learn more, visit [https://docs.feast.dev/](https://docs.feast.dev/).