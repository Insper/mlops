# DVC + S3

It is possible to use *dvc* with a *remote* pointing to an **S3** bucket.

!!! exercise text short "Question!"
    Point out at least one advantage of using **S3** as storage instead of a local folder.

    !!! answer "Answer!"
        - It facilitates collaboration between data scientists since information is centralized.

        - S3 is scalable, whereas local files can exceed the disk's storage capacity.

        - S3 is also durable and secure, with data replication capabilities.

## Practicing!

Create another repository and repeat the procedures from the previous handout.

Some important steps:

!!! exercise "Question!"
    Init *DVC*, download and track data:

    <p>
    <div class="termy">

    ```console
    $ dvc init
    $ dvc get-url https://mlops-material.s3.us-east-2.amazonaws.com/data_v0.csv  data/data.csv
    $ dvc add data/data.csv
    ```

    </div>
    </p>

!!! exercise "Question!"
    Git commit:

    <p>
    <div class="termy">

    ```console
    $ git add data/data.csv.dvc data/.gitignore
    $ git commit -m "Add data to project"
    $ git push
    ```

    </div>
    </p>

!!! exercise "Question!"
    Create a bucket on S3 with the pattern name `mlops-dvc-INSPERUSERNAME`

    !!! warning ""
        Check [**HERE**](../11-logging/write_logs_to_s3.md#create-bucket) if you need help with bucket creation.

!!! exercise "Question!"
    Configure S3 storage:

    !!! danger "Attention!"
        Change the bucket name in `mlops-dvc-INSPERUSERNAME`

    <p>
    <div class="termy">

    ```console
    $ dvc remote add myremote s3://mlops-dvc-INSPERUSERNAME
    $ dvc remote default myremote
    $ dvc push
    ```

    </div>
    </p>

!!! exercise "Question!"
    Check the contents of the bucket and ensure that the data was actually stored!

!!! warning "Attention!"
    After finishing the class, delete the bucket you created!

## References

- ML complexity image: https://dvc.org/static/d40892521e2fff94dac9e59693f366df/5cd1d/data-ver-complex.webp
- Versions image: https://dvc.org/static/39d86590fa8ead1cd1247c883a8cf2c0/aa619/project-versions.webp