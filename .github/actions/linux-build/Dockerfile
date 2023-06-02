FROM nexus.jamesjonesconsulting.com:5443/ymdllc/rhel7-python/3.11.3:latest

RUN source scl_source enable rh-ruby26 && \
    gem install ffi && \
    gem install fpm && \
    python -m pip install . && \
    pyinstaller --onefile --windowed \
        --name awsauth \
        --clean \
        --add-data "awsauth/us-east-1-signin-aws-chain.pem:awsauth" \
        --hidden-import 'timeago.locales.en' \
        awsauth.py && \
    fpm -s dir -t rpm -n awsauth -v "1.0.0-rc4" --iteration "1" \
        --description "awsauth: Allows you to use saml auth in order to access AWS apis" \
        --url "https://github.com/AllegiantTravelCo/devops-g4-aws-saml" \
        --license "custom" --vendor "Allegiant Travel Company" --maintainer "IT DevOps <itdevops@allegiantair.com>" \
        -p ./dist \
        ./dist/awsauth=/usr/bin/awsauth && \
    fpm -s dir -t rpm -n awsauth -v "1.0.0-rc4" --iteration "1" \
        --description "awsauth: Allows you to use saml auth in order to access AWS apis" \
        --url "https://github.com/AllegiantTravelCo/devops-g4-aws-saml" \
        --license "custom" --vendor "Allegiant Travel Company" --maintainer "IT DevOps <itdevops@allegiantair.com>" \
        -p ./dist \
        ./dist/awsauth=/usr/bin/awsauth
