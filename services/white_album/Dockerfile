FROM mcr.microsoft.com/dotnet/sdk:5.0

COPY ./src /app

WORKDIR /app

RUN DOTNET_CLI_TELEMETRY_OPTOUT=1 dotnet restore && dotnet publish -c Release -o publish


ENV DOTNET_CLI_TELEMETRY_OPTOUT=1 COMPlus_JitTelemetry=0 COMPlus_legacyCorruptedStateExceptionsPolicy=1 COMPlus_legacyUnhandledExceptionPolicy=1

RUN adduser --system --home /app --shell /usr/sbin/nologin --no-create-home --disabled-password deployer

CMD ["dotnet", "publish/WhiteAlbum.dll"]