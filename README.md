# FastAPI Image Processor

This service asynchronously processes images, finds a place to watermark them and sends to the **Image Storage**.

### Minikube deployment tips
* you can upload local image directly into the minikube and avoid 
the need of Remote Registries
```bash
minikube image load image-processor
```
* to apply deployment, just use a regular `kubectl` command:
```bash
kubectl apply -f deployment/manifest.yml
```
* to use API outside the cluster, you can use a tunneling command from minikube:
```bash
minikube service processor-service
```
