import a2s
import valve.source
import valve.source.master_server
import socket

convar_to_look_for = input("Convar to look for: ")
convar_value_to_look_for = input("Convar value to look for: ")

with valve.source.master_server.MasterServerQuerier() as msq:
	servers_found = 0
	servers_checked = []
	try:
		for address in msq.find(region=[u"eu", "as", "na", "sa"],
								gamedir=u'tf'): #You can customize this if you wish and have an idea what you're doing (csgo, cstrike, tf, garrysmod)

			try:
				if a2s.rules(address)[convar_to_look_for] == str(convar_value_to_look_for):

					# Save the server ip:port to a file
					with open("servers.txt","a") as f:
						f.write(f"\n{address[0]}:{address[1]} --- {convar_to_look_for}")

					print(f"\n\tFound a server! IP: {address[0]}:{address[1]}\n")

					servers_found += 1
				else:

					print(f"Checking for {a2s.info(address).server_name}")

			# This gets executed when the server that we're checking timed out.
			except socket.timeout:

				print("Server {}:{} timed out!".format(*address))
				continue

	# Rare AF, if you see this error it's a miracle, but better catch it if it happens
	except valve.source.NoResponseError:
		print("Master server request timed out!")

	# Called when the server list ended. Idk why it's OSError
	except OSError:
		print(f"Found {servers_found} {convar_to_look_for} servers.")
