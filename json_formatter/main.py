import json
import pandas as pd


def extract_frame_data(data, frame_id, tracker_id, frame_rider_map):

    points = data["points"]['p1']
    attributes = data["attributes"]

    output = {
        "_id": data['_id'],
        "type": data['type'],
        "label": data['label'],
        "point_x": points['x'],
        "point_y": points['y'],
        "point_label": points['label'],
        "wearing_mask": attributes['wearing_mask']['value'],
        "wearing_shirt": attributes['wearing_shirt']['value'],
        "selfie_validity": attributes['selfie_validity']['value'],
        "rider_id": frame_rider_map[frame_id],
        "tracker_id": tracker_id
    }

    csv_data = (frame_id, data['_id'], data['label'])

    return output, csv_data


if __name__ == "__main__":
    f = open('input.json')
    data = json.load(f)

    rider_info = data['rider_info']

    frame_rider_map = {
        key: value['rider_id'] for key, value in rider_info.items()
    }

    trackers = data["maker_response"]["video2d"]["data"]["annotations"]

    output = {}
    csv_data = []
    
    for track in trackers:
        track_id = track["_id"]
        frames = track["frames"]
        
        for key, value in frames.items():

            out, csv_data_tup = extract_frame_data(data=value, frame_id=key,
                                                   tracker_id=track_id, frame_rider_map=frame_rider_map)

            csv_data.append(csv_data_tup)

            if output.get(key):
                output.get(key).append(out)
            else:
                output[key] = [out]

    final_output = {
        "export_data": {
            "annotations": {
                "frames": output
            },
            "number of annotations": len(output)
        }
    }

    with open("output.json", "wb") as f:
        f.write(json.dumps(final_output, indent=4).encode("utf-8"))

    df = pd.DataFrame(csv_data, columns=["frame_id", "tracking_id", "label"])

    df.to_csv("tracker_wise_data.csv", index=False)

    f.close()
