import os
from kubernetes import client, config

def read_configmap():
    with open('/config/applications', 'r') as f:
        applications = f.readlines()
    return [app.strip() for app in applications]

def redeploy_application(namespace, deployment_name):
    config.load_incluster_config()
    api_instance = client.AppsV1Api()
    
    # Obter o deployment atual
    deployment = api_instance.read_namespaced_deployment(deployment_name, namespace)
    
    # Modificar a anotação para forçar o redeploy
    deployment.spec.template.metadata.annotations = {
        "kubectl.kubernetes.io/restartedAt": datetime.datetime.utcnow().isoformat()
    }
    
    # Atualizar o deployment
    api_instance.patch_namespaced_deployment(deployment_name, namespace, deployment)
    print(f"Redeploy triggered for {namespace}.{deployment_name}")

def main():
    applications = read_configmap()
    for app in applications:
        namespace, deployment_name = app.split('.')
        redeploy_application(namespace, deployment_name)

if __name__ == "__main__":
    main()
