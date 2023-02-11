FROM ubuntu:latest

RUN apt-get update
RUN apt-get install openssh-server -y

RUN mkdir /var/run/sshd
#RUN echo 'root:pwd' | chpasswd
RUN useradd --create-home gst4
#RUN echo -e 'gst4\ngst4' | passwd gst4
RUN echo 'gst4:gst4' | chpasswd -
# SSH allow root login via remote
#RUN sed -i 's/#PermitRootLogin/PermitRootLogin/g' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
#RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

# RESTART SSH
# RUN /etc/init.d/ssh restart
CMD ["service", "ssh", "start", "-D"]
