import urllib.request
import os
import subprocess

JAR_URL = "https://repo1.maven.org/maven2/io/swagger/codegen/v3/swagger-codegen-cli/3.0.61/swagger-codegen-cli-3.0.61.jar"
JAR_PATH = "swagger-codegen-cli.jar"

if not os.path.exists(JAR_PATH):
    print("Downloading Swagger Codegen CLI...")
    urllib.request.urlretrieve(JAR_URL, JAR_PATH)
    print("Download complete.")

print("Generating Python Flask server...")
subprocess.run([
    "java", "-jar", JAR_PATH, "generate",
    "-i", "swagger.yaml",
    "-l", "python-flask",
    "-o", "server"
])
print("Code generation complete!")
