import timeit
import gc
from app import app

gc.disable()
client = app.test_client()

def run_tests_for_depth(depth):
    # depth parameter is the offset
    after_id = f"p{depth}"
    page = (depth // 10) + 1  # 0 -> page 1, 10 -> page 2, etc.
        
    def test_offset():
        resp = client.get(f'/v1/products?limit=10&offset={depth}')
        assert resp.status_code == 200

    def test_page():
        resp = client.get(f'/v1/products?page={page}&per_page=10')
        assert resp.status_code == 200

    def test_cursor():
        resp = client.get(f'/v1/products?limit=10&after_id={after_id}')
        assert resp.status_code == 200

    number_of_runs = 50
    offset_time = timeit.timeit(test_offset, number=number_of_runs)
    page_time = timeit.timeit(test_page, number=number_of_runs)
    cursor_time = timeit.timeit(test_cursor, number=number_of_runs)

    print(f"Depth: {depth:<7} | Offset: {offset_time:.4f}s | Page: {page_time:.4f}s | Cursor: {cursor_time:.4f}s")

if __name__ == '__main__':
    print("Generating 1M records in memory upon import (done).")
    print(f"Running benchmarking (50 requests each per depth)...")
    print("-" * 75)
    
    depths = [10, 1000, 10000, 100000, 500000, 900000]
    for d in depths:
        run_tests_for_depth(d)
