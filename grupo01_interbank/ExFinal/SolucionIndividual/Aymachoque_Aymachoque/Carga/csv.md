## (1) Crear bucket
REGION="us-east-1"
BUCKET_PREFIX="examenfinal"
BUCKET="${BUCKET_PREFIX}-$(date +%s)"
aws s3 mb "s3://$BUCKET" --region "$REGION"

<img width="1368" height="418" alt="I1" src="https://github.com/user-attachments/assets/8259b178-cd75-4b20-a3da-46c2a533fbb1" />

## (2) Crear la estructura bronce/raw, bronce/processed, bronce/curated
printf "" > .keep
aws s3 cp .keep "s3://$BUCKET/bronce/raw/.keep"
aws s3 cp .keep "s3://$BUCKET/bronce/processed/.keep"
aws s3 cp .keep "s3://$BUCKET/bronce/curated/.keep"

<img width="1919" height="707" alt="I2" src="https://github.com/user-attachments/assets/18037646-7ae1-452e-916e-a977e860269f" />


## (3) En CloudShell: Actions -> Upload file
    Subimos Sample_Superstore.csv a CloudShell

## (4) Subir el CSV a S3 por CLI
aws s3 cp "Sample_Superstore.csv" "s3://$BUCKET/bronce/raw/Sample_Superstore.csv"

<img width="1884" height="674" alt="I3" src="https://github.com/user-attachments/assets/36fd268c-6821-4e93-a54e-7ed17e11baeb" />

