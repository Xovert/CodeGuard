FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install Postfix
RUN apt-get update && \
    apt-get install -y postfix && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Configure Postfix as a send-only server:
# - Listen only on localhost
# - Do not accept incoming mail for local domains
# - No external relay host configured (adjust if needed)
RUN postconf -e "inet_interfaces = loopback-only" && \
    postconf -e "mydestination =" && \
    postconf -e "relayhost =" && \
    postconf -e "myhostname = mail.codeguard.id" && \
    postconf -e "myorigin = codeguard.id" 

# Run Postfix in the foreground so Docker keeps the container alive
CMD ["postfix", "start-fg"]

