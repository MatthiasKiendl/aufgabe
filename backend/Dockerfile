# This Dockerfile sets up a PHP 8.4 environment with Apache.
# It installs curl and downloads PHPUnit 9 as a PHAR file for testing.
# The working directory is set to /var/www/html, and all files from the build context are copied into it.
FROM php:8.4-apache

RUN apt-get update && apt-get install -y curl \
    && curl -LsS https://phar.phpunit.de/phpunit-9.phar -o /usr/local/bin/phpunit \
    && chmod +x /usr/local/bin/phpunit

WORKDIR /var/www/html
COPY . .
