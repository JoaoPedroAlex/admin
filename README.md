# admin
Project for automating WAS administration

The purpose of this document is to help you understand how to use this framework.

This framework was built using Ant to automate tasks.

First step 
Download all the code to a file setup.zip
Create a installation directory which will be used through this framework as ${basedir}
Extract the setup.zip file to this directory.

To use the setup command in Windows edit first the ${basedir}/bin/install.properties.bat and ${basedir}/scripts/general-config.properties to set the environment variables.
Edit the ${basedir}/scripts/was-config.properties to set the parameters needed to connect to WAS.

You should set the admin user / password in your soap.client.props for security reasons otherwise you should set the passowrd in file was-config.properties and execute the tool PropFilePasswordEncoder to encrypt the password so that ii is not visible to whoever read the file.
