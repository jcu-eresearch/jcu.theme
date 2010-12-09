def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('jcu.theme_various.txt') is None:
        return

    # Add additional setup code here
    try:
        from collective.recaptcha.settings import getRecaptchaSettings
        settings = getRecaptchaSettings()
        settings.public_key = u'6Ld5c78SAAAAAJH6NdN69ZYiXGrYcs9MLrvjY08U'
        settings.private_key = u'6Ld5c78SAAAAAGJpMrcbF_vAzeVRNWCjIWFZPZfs'
    except:
        pass



