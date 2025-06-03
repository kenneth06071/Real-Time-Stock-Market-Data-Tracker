from CSCI_2100_project import stock_tracker

class NaiveStockTracker:
    def __init__(self):
        self.stocks = {}

    def insert(self, id, price):
        if id not in self.stocks:
            self.stocks[id] = {"price": price, "volume": 0}

    def update_price(self, id, price):
        if id in self.stocks:
            self.stocks[id]["price"] = price

    def increase_volume(self, id, vinc):
        if id in self.stocks:
            self.stocks[id]["volume"] += vinc

    def lookup(self, id):
        return self.stocks.get(id, None)

    def price_range(self, p1, p2):
        return sorted([id for id, s in self.stocks.items() if p1 <= s["price"] <= p2])

    def max_vol(self):
        if not self.stocks:
            return None

        max_volume = max(stock["volume"] for stock in self.stocks.values())

    # Filter to all stocks with max volume
        max_candidates = [id for id, stock in self.stocks.items() if stock["volume"] == max_volume]

    # Return the one with the maximum ID
        max_id = max(max_candidates)

        return [max_id, max_volume]

def run_test_file(filename="test_ops.txt", log_file="validation_log.txt"):
    tracker = stock_tracker()
    naive = NaiveStockTracker()
    issues = []

    with open(filename, 'r') as f:
        for line_num, line in enumerate(f, 1):
            tokens = line.strip().split()
            if not tokens:
                continue

            try:
                cmd = tokens[0]

                if cmd == "insert":
                    id, price = int(tokens[1]), float(tokens[2])
                    tracker.insert_new_stock(id, price)
                    naive.insert(id, price)

                elif cmd == "update_price":
                    id, price = int(tokens[1]), float(tokens[2])
                    tracker.update_price(id, price)
                    naive.update_price(id, price)

                elif cmd == "increase_volume":
                    id, vinc = int(tokens[1]), int(tokens[2])
                    tracker.increase_volume(id, vinc)
                    naive.increase_volume(id, vinc)

                elif cmd == "lookup":
                    id = int(tokens[1])
                    actual = tracker.lookup_by_id(id)
                    expected = naive.lookup(id)

                    if expected is None and actual is None:
                        continue
                    elif expected is None or actual is None:
                        issues.append(f"[Mismatch] Line {line_num}: lookup {id} → Expected: {expected}, Got: {actual}")
                    else:
                        expected_tuple = (id, expected["price"], expected["volume"])
                        if actual != expected_tuple:
                            issues.append(f"[Mismatch] Line {line_num}: lookup {id} → Expected: {expected_tuple}, Got: {actual}")

                elif cmd == "price_range":
                    p1, p2 = float(tokens[1]), float(tokens[2])
                    actual = sorted(tracker.price_range(p1, p2))
                    expected = naive.price_range(p1, p2)
                    if actual != expected:
                        issues.append(f"[Mismatch] Line {line_num}: price_range({p1}, {p2}) → Expected: {expected}, Got: {actual}")

                elif cmd == "max_vol":
                    actual = tracker.max_vol()
                    expected = naive.max_vol()
                    if actual != expected:
                        issues.append(f"[Mismatch] Line {line_num}: max_vol → Expected: {expected}, Got: {actual}")

            except Exception as e:
                issues.append(f"[ERROR] Line {line_num}: {line.strip()} → {e}")

    with open(log_file, "w") as log:
        if not issues:
            log.write("All operations passed successfully.\n")
            print("All operations passed successfully.")
        else:
            log.write(f" {len(issues)} issues found during validation:\n")
            for issue in issues:
                log.write(issue + "\n")
            print(f" {len(issues)} issues written to '{log_file}'.")

if __name__ == "__main__":
    run_test_file()