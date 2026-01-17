"""
Single script to run the entire Novel RAG pipeline end-to-end
Starts servers, waits for readiness, generates predictions
"""

import subprocess
import time
import requests
import sys
import os


def check_docker_installed():
    """Check if Docker is installed"""
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
        subprocess.run(["docker-compose", "--version"], capture_output=True, check=True)
        return True
    except:
        print("❌ Docker or docker-compose not found!")
        print("   Please install Docker Desktop from https://www.docker.com/")
        return False


def check_server_ready(host, port, max_retries=30, retry_delay=5):
    """Check if Pathway server is ready"""
    url = f"http://{host}:{port}/v1/retrieve"
    
    for attempt in range(max_retries):
        try:
            response = requests.post(
                url,
                json={"query": "test", "k": 1},
                timeout=10
            )
            if response.status_code == 200:
                return True
        except:
            pass
        
        if attempt < max_retries - 1:
            print(f"   Waiting for server on port {port}... ({attempt+1}/{max_retries})")
            time.sleep(retry_delay)
    
    return False


def start_servers():
    """Start Docker containers"""
    print("🚀 Starting Docker containers...")
    
    try:
        result = subprocess.run(
            ["docker-compose", "up", "-d", "--build"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            print(f"❌ Failed to start containers: {result.stderr}")
            return False
        
        print("✅ Docker containers started")
        return True
    except Exception as e:
        print(f"❌ Error starting containers: {e}")
        return False


def wait_for_servers():
    """Wait for both Pathway servers to be ready"""
    from config.config import PATHWAY_HOST, PATHWAY_PORT_CASTAWAYS, PATHWAY_PORT_MONTE_CRISTO
    
    print("\n⏳ Waiting for Pathway servers to be ready...")
    print("   This may take 1-2 minutes for initial indexing...\n")
    
    print("📚 Checking Castaways server (port 8765)...")
    if not check_server_ready(PATHWAY_HOST, PATHWAY_PORT_CASTAWAYS):
        print(f"❌ Castaways server not ready after 2.5 minutes")
        return False
    print("✅ Castaways server ready!\n")
    
    print("📚 Checking Monte Cristo server (port 8766)...")
    if not check_server_ready(PATHWAY_HOST, PATHWAY_PORT_MONTE_CRISTO):
        print(f"❌ Monte Cristo server not ready after 2.5 minutes")
        return False
    print("✅ Monte Cristo server ready!\n")
    
    return True


def run_pipeline():
    """Run the main prediction pipeline"""
    print("="*80)
    print("🎯 Running prediction pipeline...")
    print("="*80 + "\n")
    
    from Code.main import main
    
    try:
        main()
        print("\n" + "="*80)
        print("✅ Pipeline completed successfully!")
        print("📄 Results saved to: results.csv")
        print("="*80)
        return True
    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main orchestration function"""
    print("="*80)
    print("🚀 Novel RAG End-to-End Pipeline")
    print("="*80 + "\n")
    
    if not check_docker_installed():
        sys.exit(1)
    
    if not start_servers():
        print("\n❌ Failed to start servers. Check Docker logs:")
        print("   docker-compose logs -f")
        sys.exit(1)
    
    if not wait_for_servers():
        print("\n❌ Servers did not become ready. Check Docker logs:")
        print("   docker-compose logs -f")
        sys.exit(1)
    
    if not run_pipeline():
        sys.exit(1)
    
    print("\n✨ All done! Check results.csv for predictions.")


if __name__ == "__main__":
    main()
