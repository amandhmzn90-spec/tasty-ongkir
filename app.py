from flask import Flask, request, jsonify
from flask_cors import CORS
import serpapi

app = Flask(__name__)
CORS(app)

client = serpapi.Client(api_key="3e4229f21d41a3441247e3feba3e654e1506ca24a86d46c4607f384abc47dc06")

START_ADDR = "Lalu Thrift, Jl. Wijaya Kusuma, Joho, Sumberejo, Kec. Ngasem, Kabupaten Kediri, Jawa Timur 64182"

@app.route('/ongkir', methods=['POST'])
def hitung_ongkir():
    data = request.json
    end_addr = data.get('alamat')

    print("\n=== REQUEST MASUK ===")
    print("Alamat tujuan:", end_addr)

    if not end_addr:
        print("❌ Alamat kosong")
        return jsonify({"error": "Alamat kosong"}), 400

    try:
        results = client.search({
            "engine": "google_maps_directions",
            "start_addr": START_ADDR,
            "end_addr": end_addr
        })

        print("\n=== RESPONSE DARI SERPAPI ===")
        print(results)

        distance = results["directions"][0]["distance"]
        km = distance / 1000

        ongkir = km * 1500
        ongkir_rounded = round(ongkir / 1000) * 1000

        print("\n=== HASIL PERHITUNGAN ===")
        print(f"Jarak (meter): {distance}")
        print(f"Jarak (km): {km}")
        print(f"Ongkir asli: {ongkir}")
        print(f"Ongkir bulat: {ongkir_rounded}")

        return jsonify({
            "km": round(km, 2),
            "ongkir": ongkir_rounded
        })

    except Exception as e:
        print("\n❌ ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)