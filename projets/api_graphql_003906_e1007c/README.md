yml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gqlgen-api
spec:
  replicas: 1
  selector:
    matchLabels:
      app: gqlgen-api
  template:
   .metadata:
      labels:
        app: gqlgen-api
    spec:
      containers:
      - name: gqlgen-api
        image: ghcr.io/trentm/gqlgen:v1.3.5
        ports:
        - containerPort: 8080
        volumeMounts:
        - name: gqlgen-api-pg-config
          mountPath: /etc/postgresql/gqlgen-api/pg-config
        - name: gqlgen-api-jwt-config
          mountPath: /etc/postgresql/gqlgen-api/jwt-config
        env:
        - name: PGDATA
          value: /var/lib/postgresql/data
        - name: PGUSER
          value: gqlgen-api
        - name: PGPASSWORD
          value: gqlgen-api-password
        - name: JWT_SECRET
          value: <your_jwt_secret>
      volumes:
      - name: gqlgen-api-pg-config
        configMap:
          name: gqlgen-api-pg-config
      - name: gqlgen-api-jwt-config
        configMap:
          name: gqlgen-api-jwt-config
  strategy:
    type: Recreate
