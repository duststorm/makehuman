// Capapbilities.mm
#import "Capabilities.h"
#import <Carbon/Carbon.h>
#include <sys/sysctl.h>
#include <dlfcn.h>

typedef const char* (*Py_GetVersionStub)();

uint32_t getInstalledPythonVer()
{
    uint32_t version = 0;

	void* libHd = ::dlopen("/Library/Frameworks/Python.framework/Python", RTLD_LAZY);
//	fprintf(stderr, "libHd is %p\n", libHd);
	if (libHd)
	{
		Py_GetVersionStub symbol = (Py_GetVersionStub)::dlsym(libHd, "Py_GetVersion");

		if (symbol)
		{
			const char * versionStr =  symbol();
			int major=0, minor=0, level=0;
//          	fprintf(stderr, "versionStr is %s\n", versionStr);

              ::sscanf(versionStr, "%d.%d.%d", &major, &minor, &level);

			version = ((major & 0xff) << 16) | ((minor & 0xff) << 8) | ((level & 0xff) << 0);
		}
		::dlclose(libHd);
	}
	return version;
}

static uint32_t getCPUInfo()
{
    uint32_t cpuType = 0;
    size_t size(sizeof(cpuType));

    int rc = ::sysctlbyname("hw.cputype", &cpuType, &size, NULL, 0);
    return ( 0 == rc ) ? cpuType : 0;
}

int getNrOfCpuCores()
{
    uint32_t nrOfCpus;
    size_t size(sizeof(nrOfCpus));

    const int rc ( ::sysctlbyname("hw.ncpu", &nrOfCpus, &size, NULL, 0) );
    return ( 0 == rc ) ? nrOfCpus : 0;
}

bool hasSIMD()
{
    uint32_t vectorExists;
    size_t size(sizeof(vectorExists));

    const int rc ( ::sysctlbyname("hw.vectorunit", &vectorExists, &size, NULL, 0) );
    return ( 0 == rc ) ? vectorExists : false;
}

bool hasSSE()
{
#if defined(__i386__) || defined(__x86_64__)
    return hasSIMD();
#else
    return false;
#endif
}

bool hasAltiVec()
{
#if defined(__ppc__) || defined(__ppc64__)
    return hasSIMD();
#else
    return false;
#endif
}

bool isArchPPC32()
{
#if defined(__ppc__) || defined(__ppc64__)
    return CPU_TYPE_POWERPC == getCPUInfo();
#else
    return false;
#endif
}

bool isArchPPC64()
{
#if defined(__ppc__) || defined(__ppc64__)
    return CPU_TYPE_POWERPC64 == getCPUInfo();
#else
    return false;
#endif
}

bool isArchIA32()
{
#if defined(__i386__) || defined(__x86_64__)
    return CPU_TYPE_I386 == getCPUInfo();
#else
    return false;
#endif
}

bool isArchIA64()
{
#if defined(__i386__) || defined(__x86_64__)
    return CPU_TYPE_X86_64 == getCPUInfo();
#else
    return false;
#endif
}

bool isArchIntel86()
{
#if defined(__i386__) || defined(__x86_64__)
    return true;
#else
    return false;
#endif
}

bool isArchPPC()
{
#if defined(__ppc__) || defined(__ppc64__)
    return true;
#else
    return false;
#endif
}

bool isArchARM()
{
#if defined(__arm__)
    return CPU_TYPE_ARM == getCPUInfo();
#else
    return false;
#endif
}

static bool getOSXVersion(SInt32& systemVersion,
                          SInt32& majorVersion,
                          SInt32& minorVersion,
                          SInt32& bugfixVersion )
{
    if ( noErr != ::Gestalt(gestaltSystemVersion, &systemVersion) )
        goto error;

    if ( noErr != ::Gestalt(gestaltSystemVersionMajor, &majorVersion) )
        goto error;

    if ( noErr != ::Gestalt(gestaltSystemVersionMinor, &minorVersion) )
        goto error;

    if ( noErr != ::Gestalt(gestaltSystemVersionBugFix, &bugfixVersion) )
        goto error;

    return true;

error:
    systemVersion = majorVersion = minorVersion = bugfixVersion = 0;
    return false;
}

// Leopard is OS X 10.5.x
bool isOSXLeopard()
{
    SInt32 sysV, majorV, minorV, debugV;

    if (true == getOSXVersion(sysV, majorV, minorV, debugV))
    {
        return ( 10 == majorV ) && ( 5 == minorV );
    }
    return false;
}

// Snow Leopard is OS X 10.6.x
bool isOSXSnowLeopard()
{
    SInt32 sysV, majorV, minorV, debugV;

    if (true == getOSXVersion(sysV, majorV, minorV, debugV))
    {
        return ( 10 == majorV ) && ( 6 == minorV );
    }
    return false;
}

// Lion is OS X 10.7.x
bool isOSXLion()
{
    SInt32 sysV, majorV, minorV, debugV;

    if (true == getOSXVersion(sysV, majorV, minorV, debugV))
    {
        return ( 10 == majorV ) && ( 7 == minorV );
    }
    return false;
}

bool supportsGCD()
{
#ifdef GCD_AVAILABLE
    SInt32 sysV, majorV, minorV, debugV;

    // GCD is supported beginning from Mac OS X 10.6 (Snow Leopard)
    if (true == getOSXVersion(sysV, majorV, minorV, debugV))
    {
        if ( majorV < 10 )
            return false;
        if ( majorV > 10 )
            return true;

        return (minorV >= 6);
    }
    return false;
#else
    return false;
#endif
}
