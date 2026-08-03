import os
import shutil
import subprocess
import stat

# Repositories to clone
REPOS = {
    "atp": "https://github.com/Tennismylife/TML-Database.git",
    "mcp": "https://github.com/JeffSackmann/tennis_MatchChartingProject.git"
}

RAW_DATA_DIR = os.path.join("data", "raw")
TEMP_DIR = os.path.join("data", "temp_clones")


def remove_readonly(func, path, exc_info):
    """Clears the read-only attribute on Windows files so rmtree can delete them."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def clone_repo(repo_url: str, target_dir: str):
    """Performs a lightweight git clone."""
    print(f"Cloning {repo_url} ...")
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir, onerror=remove_readonly)
        
    env = os.environ.copy()
    env['GIT_HTTP_MAX_REQUEST_BUFFER'] = '100M'

    subprocess.run(
        ["git", "clone", "--depth", "1", repo_url, target_dir],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env
    )
    print(f" Successfully cloned to {target_dir}")


def find_and_copy_file(source_dir: str, keyword: str, dest_path: str) -> bool:
    """Recursively searches a directory for a file containing a keyword and copies it."""
    for root, _, files in os.walk(source_dir):
        for file in files:
            if keyword.lower() in file.lower() and file.endswith(".csv"):
                src_path = os.path.join(root, file)
                shutil.copyfile(src_path, dest_path)
                print(f" Copied -> {dest_path} (matched: {file})")
                return True
    print(f" Warning: Could not find file matching '{keyword}'")
    return False


def ingest_bronze_data():
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    print("--- Starting Bronze Data Ingestion ---")
    
    # 1. Clone ATP repo
    atp_temp = os.path.join(TEMP_DIR, "atp")
    clone_repo(REPOS["atp"], atp_temp)
    
    find_and_copy_file(atp_temp, "ATP_Database", os.path.join(RAW_DATA_DIR, "atp_players_tml.csv"))
    find_and_copy_file(atp_temp, "2023", os.path.join(RAW_DATA_DIR, "atp_matches_2023.csv"))
    find_and_copy_file(atp_temp, "2024", os.path.join(RAW_DATA_DIR, "atp_matches_2024.csv"))
    
    # 2. Clone Match Charting Project repo
    mcp_temp = os.path.join(TEMP_DIR, "mcp")
    clone_repo(REPOS["mcp"], mcp_temp)
    
    find_and_copy_file(mcp_temp, "charting-m-matches", os.path.join(RAW_DATA_DIR, "charting_m_matches.csv"))
    find_and_copy_file(mcp_temp, "charting-m-points-2020s", os.path.join(RAW_DATA_DIR, "charting_m_points_2020s.csv"))
    
    # Clean up temporary clone directory with Windows permission handling
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR, onerror=remove_readonly)
        
    print("--- Bronze Data Ingestion Complete ---")


if __name__ == "__main__":
    ingest_bronze_data()