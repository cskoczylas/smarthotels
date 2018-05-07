# Mount the docker cert volumes and then request the cert.
docker run -it --rm \
      -v smarthotels_certs:/etc/letsencrypt \
      -v smarthotels_certs-data:/data/letsencrypt \
      deliverous/certbot \
      certonly \
      --webroot --webroot-path=/data/letsencrypt \
      -d aws.sdp.infante.xyz