from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS for cross-origin requests from the static HTML site
CORS(app)

@app.route('/classify', methods=['POST'])
def classify():
    data = request.get_json()
    if not data or 'ip' not in data:
        return jsonify({'success': False, 'error': 'No IP address provided'}), 400
        
    ip = data['ip'].strip()
    
    try:
        parts = ip.split('.')
        if len(parts) != 4:
            return jsonify({'success': False, 'error': 'Invalid format. Use IPv4 standard (e.g., 192.168.1.1)'}), 400
            
        first_octet = int(parts[0])
        
        # Verify all octets are valid integers between 0 and 255
        for part in parts:
            if not (0 <= int(part) <= 255):
                return jsonify({'success': False, 'error': 'Octets must be between 0 and 255'}), 400

        if first_octet == 0:
            ip_class = 'Invalid (0.x.x.x)'
            description = 'Used for broadcast messages to the current network'
        elif 1 <= first_octet <= 126:
            ip_class = 'Class A'
            description = 'Network bits: 8, Host bits: 24 (Default Subnet: 255.0.0.0)'
        elif first_octet == 127:
            ip_class = 'Loopback'
            description = 'Reserved for loopback testing (e.g., localhost)'
        elif 128 <= first_octet <= 191:
            ip_class = 'Class B'
            description = 'Network bits: 16, Host bits: 16 (Default Subnet: 255.255.0.0)'
        elif 192 <= first_octet <= 223:
            ip_class = 'Class C'
            description = 'Network bits: 24, Host bits: 8 (Default Subnet: 255.255.255.0)'
        elif 224 <= first_octet <= 239:
            ip_class = 'Class D'
            description = 'Reserved for Multicast groups'
        elif 240 <= first_octet <= 255:
            ip_class = 'Class E'
            description = 'Reserved for Future/Experimental use'
        else:
            ip_class = 'Unknown'
            description = 'Out of standard IPv4 ranges'

        return jsonify({
            'success': True,
            'ip': ip,
            'class': ip_class,
            'description': description
        })
        
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid characters in IP address'}), 400

if __name__ == '__main__':
    print("==================================================")
    print(" Starting NatIvyberNotes IP Classifier Backend    ")
    print(" Make sure to install dependencies:               ")
    print(" pip install flask flask-cors                     ")
    print("==================================================")
    app.run(host='127.0.0.1', port=5000, debug=True)
