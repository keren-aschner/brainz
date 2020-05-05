FROM nikolaik/python-nodejs:python3.8-nodejs14

EXPOSE 8080

COPY scripts/wait-for-it.sh /
RUN chmod 755 wait-for-it.sh

WORKDIR /brainz-gui

COPY brainz-gui/package.json .
COPY brainz-gui/package-lock.json .
RUN npm install --silent
RUN npm install react-scripts@3.4.1 -g --silent

COPY brainz-gui/ /brainz-gui
RUN npm run build

WORKDIR /

COPY requirements.txt /
RUN pip3.8 install -r requirements.txt

COPY brainz /brainz
RUN mv /brainz-gui/build /brainz/gui
