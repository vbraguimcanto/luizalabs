FROM postgres:12
LABEL maintainer = "Victor Canto"
ENV POSTGRES_USER luizalabs
ENV POSTGRES_PASSWORD t3st@lu1z4l4bs
ENV POSTGRES_DB luizalabs
EXPOSE 5432