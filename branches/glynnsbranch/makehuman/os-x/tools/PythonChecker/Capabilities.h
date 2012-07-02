#ifndef _Capabilities_H_
#define _Capabilities_H_ "808DE683-0C85-474F-872E-25203F9DD61D"

// Capapbilities.h
#import <CoreServices/CoreServices.h>

int getNrOfCpuCores();

uint32_t getInstalledPythonVer();

inline bool isPyInstalled25()
{
	const uint32_t v ( getInstalledPythonVer() );

	return (2 == (uint8_t)(v >> 16)) &&
           (5 == (uint8_t)(v >> 8));
}

inline bool isPyInstalled26()
{
	const uint32_t v ( getInstalledPythonVer() );

	return (2 == (uint8_t)(v >> 16)) &&
           (6 == (uint8_t)(v >> 8));
}

inline bool isPyInstalled27()
{
	const uint32_t v ( getInstalledPythonVer() );

	return (2 == (uint8_t)(v >> 16)) &&
           (7 == (uint8_t)(v >> 8));
}

inline bool isPyInstalled30()
{
	const uint32_t v ( getInstalledPythonVer() );

	return (3 == (uint8_t)(v >> 16)) &&
           (0 == (uint8_t)(v >> 8));
}

inline bool isPyInstalled31()
{
	const uint32_t v ( getInstalledPythonVer() );

	return (3 == (uint8_t)(v >> 16)) &&
           (1 == (uint8_t)(v >> 8));
}

inline bool isPyInstalled32()
{
	const uint32_t v ( getInstalledPythonVer() );

	return (3 == (uint8_t)(v >> 16)) &&
           (2 == (uint8_t)(v >> 8));
}

inline bool isPyInstalled33()
{
	const uint32_t v ( getInstalledPythonVer() );

	return (3 == (uint8_t)(v >> 16)) &&
           (3 == (uint8_t)(v >> 8));
}

/** Check if the running host host is of the archtecture PowerPC 32 bit.
 * This includes all PPC Architectures with 32 bit. Note that
 * 64 Bit PowerPCs will not be reported by this call!
 * Use #isArchPPC64() instead!
 *
 * \return true if the hosts CPU is of the kind PowerPC 32 bit
 *
 * \see isArchPPC64()
 * \see isArchARM()
 * \see isArchI386()
 * \see isArchIA64()
 */
bool isArchPPC32();

/** Check if the running host host is of the archtecture PowerPC 64 bit.
 * This call covers only all PPC Architectures with 64 bit. Note that
 * 32 Bit PowerPCs will not be reported by this call!
 * Use #isArchPPC32() instead!
 *
 * \return true if the hosts CPU is of the kind PowerPC 64 bit (e.g G5)
 *
 * \see isArchPPC32()
 * \see isArchI386()
 * \see isArchIA64()
 *
 * \see isArchIntel86()
 * \see isArchPPC()
 * \see isArchARM()
 */
bool isArchPPC64();

/** Check if the running host host is of the archtecture IA32 (Intel 32 bit).
 * This includes all Intel x68 Architectures with 32 bit. Note that
 * IA64 will not be reported by this call! Use #isArchIA64() instead!
 *
 * \return true if the hosts CPU is of the kind IA32
 *
 * \see isArchPPC32()
 * \see isArchPPC64()
 * \see isArchIA32()
 *
 * \see isArchIntel86()
 * \see isArchPPC()
 * \see isArchARM()
 */
bool isArchIA32();

/** Check if the running host host is of the archtecture IA64 (Intel 64 bit).
 * This covers *only* all architectures with 32 bit. Note that
 * 64 Bit Intel CPUs will not be reported by this call! Use #isArchIA32() instead!
 *
 * \return true if the hosts CPU is of the kind IA64
 *
 * \see isArchPPC32()
 * \see isArchPPC64()
 * \see isArchI386()
 * \see isArchIA64()
 *
 * \see isArchIntel86()
 * \see isArchPPC()
 * \see isArchARM()
 */
bool isArchIA64();

/** Check if the running host host is either of the archtecture IA64 (Intel 64 bit) *or* IA32(Intel 64 bit).
 * This covers *all* x86 architectures!.
 *
 * \return true if the hosts CPU is of the kind IA32 or IA64
 *
 * \see isArchPPC32()
 * \see isArchPPC64()
 * \see isArchI386()
 * \see isArchIA64()
 *
 * \see isArchPPC()
 * \see isArchARM()
 */
bool isArchIntel86();

/** Check if the running host host is the architecture PowerPC.
 * This covers *all* PowerPC architectures that are 32- or 64 bits.
 *
 * \return true if the hosts CPU is of the kind PPC32 or PPC64
 *
 * \see isArchPPC32()
 * \see isArchPPC64()
 * \see isArchI386()
 * \see isArchIA64()
 *
 * \see isArchIntel86()
 * \see isArchARM()
 */
bool isArchPPC();

/** Check if the running host host is of the archtecture ARM.
 *
 * \return true if the hosts CPU is of the kind ARM.
 *
 * \see isArchPPC32()
 * \see isArchPPC64()
 * \see isArchI386()
 * \see isArchIA64()
 *
 * \see isArchIntel86()
 * \see isArchPPC()
 */
bool isArchARM();

bool hasSSE();
bool hasAltiVec();
bool hasSIMD();

/** Check if the running host is Mac OS X 10.5.x aka "Leopard"
 * \return true if the host OS is 10.5.x
 * \see isOSXLion()
 * \see isOSXSnowLeopard()
 */
bool isOSXLeopard();

/** Check if the running host is Mac OS X 10.6.x aka "Snow Leopard"
 * \return true if the host OS is 10.6.x
 * \see isOSXLion()
 * \see isOSXLeopard()
 */
bool isOSXSnowLeopard();

/** Check if the running host is Mac OS X 10.7.x aka "Lion"
 * \return true if the host OS is 10.7.x
 * \see isOSXLeopard()
 * \see isOSXSnowLeopard()
 */
bool isOSXLion();

bool supportsGCD();

#endif /* _Capabilities_H_ */
