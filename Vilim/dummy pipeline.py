import csv

def merge_outputs(bartul_file, lovre_file, output_csv):
    # Učitavanje Bartulovih podataka
    bartul_data = []
    with open(bartul_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            timestamp, class_id, ocr_value, _, _ = row
            bartul_data.append({
                "timestamp": int(timestamp),
                "class_id": int(class_id),
                "ocr_value": ocr_value,
                "generic_x": None,
                "generic_y": None
            })

    # Učitavanje Lovrinih podataka
    lovre_data = []
    with open(lovre_file, 'r') as f:
        for line in f:
            class_id, x_center, y_center, _, _ = map(float, line.strip().split())
            lovre_data.append({
                "class_id": int(class_id),
                "x_center": x_center,
                "y_center": y_center
            })

    # Spajanje podataka prema `class_id`
    for bartul_entry in bartul_data:
        for lovre_entry in lovre_data:
            if bartul_entry["class_id"] == lovre_entry["class_id"]:
                bartul_entry["generic_x"] = lovre_entry["x_center"]
                bartul_entry["generic_y"] = lovre_entry["y_center"]
                break

    # Generiranje izlaznog CSV-a
    with open(output_csv, 'w', newline='') as f:
        fieldnames = ["timestamp", "class_id", "ocr_value", "centroid_x", "centroid_y"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for entry in bartul_data:
            if entry["generic_x"] is not None and entry["generic_y"] is not None:
                writer.writerow({
                    "timestamp": entry["timestamp"],
                    "class_id": entry["class_id"],
                    "ocr_value": entry["ocr_value"],
                    "centroid_x": entry["generic_x"],
                    "centroid_y": entry["generic_y"]
                })

    print(f"Pipeline completed. Output saved to {output_csv}")

