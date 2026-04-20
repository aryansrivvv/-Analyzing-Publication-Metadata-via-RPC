import requests
import time
from multiprocessing import Pool, cpu_count
from collections import Counter


BASE_URL = "http://72.60.221.150:8080"
STUDENT_ID = "MDS202514" 

def get_secret_key():
    """Step 1: Authenticate and retrieve a dynamic Secret Key."""
    response = requests.post(f"{BASE_URL}/login", json={"student_id": STUDENT_ID})
    response.raise_for_status()
    return response.json().get("secret_key")

def get_publication_title(secret_key, filename):
    """Step 2: Use the key to retrieve the publication title with retry logic for 429s."""
    url = f"{BASE_URL}/lookup"
    payload = {"secret_key": secret_key, "filename": filename}
    
    while True:
        response = requests.post(url, json=payload)
        
        # Handle Throttling (100 req/sec limit)
        if response.status_code == 429:
            time.sleep(1.0)  # Wait 1 second before retrying
            continue
            
        if response.status_code == 200:
            return response.json().get("title", "")
        else:
            print(f"Error {response.status_code} on {filename}")
            return ""

def mapper(filename_chunk):
    """
    Map Phase: Retrieve titles for a chunk of files and yield word counts.
    Each worker gets its own secret key to avoid session conflicts.
    """
    counter = Counter()
    try:
        secret_key = get_secret_key()
    except Exception as e:
        print(f"Worker failed to authenticate: {e}")
        return counter

    for filename in filename_chunk:
        title = get_publication_title(secret_key, filename)
        if title:
            # Extract the first word (splitting by space)
            words = title.split()
            if words:
                first_word = words[0]
                counter[first_word] += 1
                
    return counter

def verify_top_10(student_id, top_10_list):
    """Step 3: Submit the computed Top 10 list for verification."""
    print(f"\nSubmitting Top 10 for verification: {top_10_list}")
    secret_key = get_secret_key()
    
    response = requests.post(
        f"{BASE_URL}/verify",
        json={"secret_key": secret_key, "top_10": top_10_list}
    )
    
    if response.status_code == 200:
        result = response.json()
        print("\n--- Verification Results ---")
        print(f"Score: {result.get('score')} / {result.get('total')}")
        print(f"Message: {result.get('message')}")
        return result
    else:
        print(f"Verification failed with status code {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    # 1. Divide filenames (pub_0.txt to pub_999.txt) into chunks
    filenames = [f"pub_{i}.txt" for i in range(1000)]
    
    # Determine number of workers and chunk sizes
    num_workers = cpu_count() * 2 # Good heuristic for network-bound tasks
    chunk_size = (len(filenames) + num_workers - 1) // num_workers
    chunks = [filenames[i:i + chunk_size] for i in range(0, len(filenames), chunk_size)]
    
    print(f"Starting map-reduce across {len(filenames)} files with {num_workers} workers...")
    
    # 2. Use multiprocessing.Pool to map the mapper function
    start_time = time.time()
    with Pool(num_workers) as p:
        mapped_counters = p.map(mapper, chunks)
        
    # 3. Combine (Reduce) the frequency counts from all workers
    final_counts = Counter()
    for worker_counter in mapped_counters:
        final_counts.update(worker_counter)
        
    # 4. Identify the Top 10 most frequent first words
    top_10_tuples = final_counts.most_common(10)
    top_10 = [word for word, count in top_10_tuples]
    
    print(f"\nProcessed in {time.time() - start_time:.2f} seconds")
    
    # 5. Call verification
    if top_10:
        verify_top_10(STUDENT_ID, top_10)
    else:
        print("Compute the top 10 words first!")