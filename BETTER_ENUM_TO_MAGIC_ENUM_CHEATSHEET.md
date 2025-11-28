# BETTER_ENUM to magic_enum Conversion Cheat Sheet

## Quick Reference - Most Common Fixes

| Error Pattern | Fix |
|---------------|-----|
| `enumVal << 16` | `static_cast<int>(enumVal) << 16` |
| `E_Type::VALUE + n` | `static_cast<E_Type>(static_cast<int>(E_Type::VALUE) + n)` |
| `enumVal._to_string()` | `string(magic_enum::enum_name(enumVal))` |
| `E_Type::_from_integral(x)` | `static_cast<E_Type>(x)` |
| `int x = enumVal;` | `int x = static_cast<int>(enumVal);` |

---

## Common Compilation Errors and Fixes

### 1. **Bitwise/Arithmetic Operations on Enum**

#### Error:
```
error: no match for 'operator<<' (operand types are 'const E_Sys' and 'int')
   int intval = (sys << 16) + (prn << 8);
                ~~~ ^~ ~~

error: no match for 'operator+' (operand types are 'E_StateComponent' and 'const int')
   component = E_StateComponent::XP + num;
               ~~~~~~~~~~~~~~~~~~~~ ^ ~~~
```

#### Fix:
Cast enum to its underlying type for operations:
```cpp
// Before (BETTER_ENUM)
int intval = (sys << 16) + (prn << 8);
component = E_StateComponent::X + num;

// After (magic_enum)
int intval = (static_cast<int>(sys) << 16) + (prn << 8);
component = static_cast<E_StateComponent>(static_cast<int>(E_StateComponent::X) + num);
```

**Pattern:** For `enum + int` that returns an enum:
```cpp
// Generic pattern
result_enum = static_cast<EnumType>(static_cast<int>(EnumType::VALUE) + offset);
```

---

### 2. **Converting Integer to Enum (_from_integral)**

#### Error:
```
error: 'E_Sys' has no member named '_from_integral'
   sys = E_Sys::_from_integral(value);
         ~~~~~~~^~~~~~~~~~~~~~
```

#### Fix:
Use `static_cast`:
```cpp
// Before (BETTER_ENUM)
sys = E_Sys::_from_integral((intval >> 16) & 0xFF);

// After (magic_enum)
sys = static_cast<E_Sys>((intval >> 16) & 0xFF);
```

**Alternative with validation:**
```cpp
// Using magic_enum to validate
auto sys_opt = magic_enum::enum_cast<E_Sys>(intval);
if (sys_opt.has_value()) {
    sys = sys_opt.value();
} else {
    // Handle invalid value
    sys = E_Sys::NONE;
}
```

---

### 3. **Converting Enum to String (_to_string)**

#### Error:
```
error: 'E_Sys' has no member named '_to_string'
   return sys._to_string();
          ~~~^~~~~~~~~~~
```

#### Fix:
Use `magic_enum::enum_name()`:
```cpp
// Before (BETTER_ENUM)
string sysName() const { return sys._to_string(); }

// After (magic_enum)
string sysName() const { return string(magic_enum::enum_name(sys)); }
```

**Note:** `magic_enum::enum_name()` returns `string_view`, so wrap with `string()` if you need `std::string`.

**Better approach - Create a helper function:**
```cpp
// Add to a common header file (e.g., enumHelpers.hpp or enums.h)
template<typename E>
inline std::string enum_to_string(E value) {
    return std::string(magic_enum::enum_name(value));
}

// Then use it simply:
string sysName() const { return enum_to_string(sys); }
```

---

### 4. **Converting Enum to Integer**

#### Error:
```
error: cannot convert 'E_Sys' to 'int' in assignment
   int sysInt = sys;
```

#### Fix:
Use `static_cast`:
```cpp
// Before (BETTER_ENUM - implicit conversion)
int sysInt = sys;

// After (magic_enum)
int sysInt = static_cast<int>(sys);
```

---

### 5. **Parsing String to Enum (_from_string)**

#### Before (BETTER_ENUM):
```cpp
E_Sys sys = E_Sys::_from_string(str);
```

#### After (magic_enum):
```cpp
auto sys_opt = magic_enum::enum_cast<E_Sys>(str);
if (sys_opt.has_value()) {
    E_Sys sys = sys_opt.value();
}

// Or with default fallback
E_Sys sys = magic_enum::enum_cast<E_Sys>(str).value_or(E_Sys::NONE);
```

---

### 6. **Comparing Enums (Should work as-is)**

These should work without changes:
```cpp
if (sys == E_Sys::GPS) { }
if (sys != E_Sys::NONE) { }

switch (sys) {
    case E_Sys::GPS: break;
    case E_Sys::GLO: break;
}
```

---

### 7. **Iterating Over Enum Values (_values)**

#### Before (BETTER_ENUM):
```cpp
for (auto sys : E_Sys::_values()) {
    // ...
}
```

#### After (magic_enum):
```cpp
for (auto sys : magic_enum::enum_values<E_Sys>()) {
    // ...
}
```

---

### 8. **Getting Enum Count (_size)**

#### Before (BETTER_ENUM):
```cpp
size_t count = E_Sys::_size();
```

#### After (magic_enum):
```cpp
size_t count = magic_enum::enum_count<E_Sys>();
```

---

### 9. **Checking if String is Valid Enum (_is_valid)**

#### Before (BETTER_ENUM):
```cpp
if (E_Sys::_is_valid(str)) {
    // ...
}
```

#### After (magic_enum):
```cpp
if (magic_enum::enum_cast<E_Sys>(str).has_value()) {
    // ...
}
```

---

### 10. **Checking if Integer is Valid Enum**

#### Before (BETTER_ENUM):
```cpp
if (E_Sys::_is_valid(value)) {
    // ...
}
```

#### After (magic_enum):
```cpp
if (magic_enum::enum_cast<E_Sys>(value).has_value()) {
    // ...
}

// Or check the range
auto sys = static_cast<E_Sys>(value);
if (magic_enum::enum_contains(sys)) {
    // ...
}
```

---

## Summary of Common Patterns

| Operation | BETTER_ENUM | magic_enum |
|-----------|-------------|------------|
| Enum → Int | `int x = enumVal;` | `int x = static_cast<int>(enumVal);` |
| Int → Enum | `E_Type::_from_integral(x)` | `static_cast<E_Type>(x)` |
| Enum → String | `enumVal._to_string()` | `magic_enum::enum_name(enumVal)` or `string(magic_enum::enum_name(enumVal))` |
| String → Enum | `E_Type::_from_string(str)` | `magic_enum::enum_cast<E_Type>(str)` |
| Enum Count | `E_Type::_size()` | `magic_enum::enum_count<E_Type>()` |
| Iterate Values | `E_Type::_values()` | `magic_enum::enum_values<E_Type>()` |
| Check Valid | `E_Type::_is_valid(x)` | `magic_enum::enum_cast<E_Type>(x).has_value()` |
| Enum + Int → Enum | `E_Type::VALUE + n` | `static_cast<E_Type>(static_cast<int>(E_Type::VALUE) + n)` |
| Enum Bitwise Op | `sys << 16` | `static_cast<int>(sys) << 16` |

---

## Quick Fix Patterns

### Pattern 1: Enum arithmetic returning int
```cpp
// OLD: int result = enumVal << 16;
int result = static_cast<int>(enumVal) << 16;
```

### Pattern 2: Enum arithmetic returning enum
```cpp
// OLD: newEnum = E_Type::START + offset;
newEnum = static_cast<E_Type>(static_cast<int>(E_Type::START) + offset);
```

### Pattern 3: Chained conversions
```cpp
// OLD: code = E_StateComponent::_from_integral(component)._to_string();
code = string(magic_enum::enum_name(static_cast<E_StateComponent>(component)));
```

---

## Additional Notes

1. **Include Header**: Add `#include "3rdparty/magic_enum.hpp"` where needed
2. **Namespace**: All magic_enum functions are in `magic_enum::` namespace
3. **Return Types**: Many magic_enum functions return `std::optional<>` for safety
4. **String Views**: Functions like `enum_name()` return `string_view`, convert to `string` if needed
5. **Constexpr**: Most magic_enum operations are `constexpr` when possible

---

## Debugging Tips

- Use `magic_enum::enum_type_name<E_Type>()` to get the enum type name as a string
- Use `magic_enum::enum_names<E_Type>()` to get all enum names as an array
- Maximum enum range is 256 by default (can be configured with `MAGIC_ENUM_RANGE_MIN/MAX`)

---

## Recommended Helper Functions

Create these helper functions in a common header (e.g., `enumHelpers.hpp`) to simplify conversions:

```cpp
#pragma once
#include "3rdparty/magic_enum.hpp"
#include <string>

// Enum to string conversion
template<typename E>
inline std::string enum_to_string(E value) {
    return std::string(magic_enum::enum_name(value));
}

// String to enum conversion with default fallback
template<typename E>
inline E string_to_enum(const std::string& str, E default_value = E{}) {
    return magic_enum::enum_cast<E>(str).value_or(default_value);
}

// Integer to enum conversion with validation
template<typename E>
inline std::optional<E> int_to_enum(int value) {
    return magic_enum::enum_cast<E>(value);
}

// Integer to enum with default fallback
template<typename E>
inline E int_to_enum_safe(int value, E default_value = E{}) {
    return magic_enum::enum_cast<E>(value).value_or(default_value);
}

// Enum arithmetic helper - add offset to enum
template<typename E>
inline E enum_add(E base, int offset) {
    return static_cast<E>(static_cast<int>(base) + offset);
}

// Enum to int helper
template<typename E>
inline int enum_to_int(E value) {
    return static_cast<int>(value);
}
```

**Usage examples:**
```cpp
// Instead of: string(magic_enum::enum_name(sys))
string name = enum_to_string(sys);

// Instead of: magic_enum::enum_cast<E_Sys>(str).value_or(E_Sys::NONE)
E_Sys sys = string_to_enum<E_Sys>(str, E_Sys::NONE);

// Instead of: static_cast<E_StateComponent>(static_cast<int>(E_StateComponent::X) + num)
E_StateComponent comp = enum_add(E_StateComponent::X, num);

// Instead of: static_cast<int>(sys)
int sysInt = enum_to_int(sys);
```

---

## File Changes Made

1. `/home/sebastien/Dev/GA/ginan/src/cpp/common/enums.h`:
   - Changed all `BETTER_ENUM(...)` to `enum class ... { }`
   - Changed include from `"3rdparty/enum.h"` to `"3rdparty/magic_enum.hpp"`

2. `/home/sebastien/Dev/GA/ginan/src/cpp/common/satSys.hpp`:
   - Fixed bitwise operations: `(sys << 16)` → `(static_cast<int>(sys) << 16)`
   - Fixed `_from_integral()` → `static_cast<E_Sys>()`
   - Fixed `._to_string()` → `magic_enum::enum_name()`
