// tests/test_framework.h — minimal header-only test harness.
//
// Council module: A9 (tests). Stdlib-only, no external deps. Each test file
// registers TEST_CASE(...) functions and calls lqttest::run_all() in main().
#pragma once

#include <cmath>
#include <cstdio>
#include <exception>
#include <functional>
#include <string>
#include <vector>

namespace lqttest {

struct Case {
    std::string name;
    std::function<void()> fn;
};

inline std::vector<Case>& registry() {
    static std::vector<Case> cases;
    return cases;
}

struct AutoReg {
    AutoReg(const char* name, std::function<void()> fn) {
        registry().push_back(Case{name, std::move(fn)});
    }
};

class Failure : public std::exception {
public:
    explicit Failure(std::string msg) : msg_(std::move(msg)) {}
    const char* what() const noexcept override { return msg_.c_str(); }
private:
    std::string msg_;
};

inline int run_all() {
    int passed = 0, failed = 0;
    std::printf("================ LQT TEST RUN ================\n");
    for (auto& c : registry()) {
        try {
            c.fn();
            std::printf("[ PASS ] %s\n", c.name.c_str());
            ++passed;
        } catch (const std::exception& e) {
            std::printf("[ FAIL ] %s\n         -> %s\n", c.name.c_str(), e.what());
            ++failed;
        } catch (...) {
            std::printf("[ FAIL ] %s\n         -> unknown exception\n", c.name.c_str());
            ++failed;
        }
    }
    std::printf("---------------------------------------------\n");
    std::printf("Total: %d   Passed: %d   Failed: %d\n", passed + failed, passed, failed);
    std::printf("=============================================\n");
    return failed == 0 ? 0 : 1;
}

} // namespace lqttest

#define LQT_CONCAT_(a, b) a##b
#define LQT_CONCAT(a, b) LQT_CONCAT_(a, b)

#define TEST_CASE(name)                                                       \
    static void name();                                                       \
    static ::lqttest::AutoReg LQT_CONCAT(autoreg_, name)(#name, name);        \
    static void name()

#define CHECK(cond)                                                           \
    do {                                                                      \
        if (!(cond)) {                                                        \
            throw ::lqttest::Failure(std::string("CHECK failed: " #cond) +    \
                                     " @ " __FILE__ ":" + std::to_string(__LINE__)); \
        }                                                                     \
    } while (0)

#define CHECK_MSG(cond, msg)                                                  \
    do {                                                                      \
        if (!(cond)) {                                                        \
            throw ::lqttest::Failure(std::string(msg) +                       \
                                     " @ " __FILE__ ":" + std::to_string(__LINE__)); \
        }                                                                     \
    } while (0)

#define CHECK_EQ(a, b)                                                        \
    do {                                                                      \
        auto _va = (a);                                                       \
        auto _vb = (b);                                                       \
        if (!(_va == _vb)) {                                                  \
            throw ::lqttest::Failure(std::string("CHECK_EQ failed: " #a " == " #b) + \
                                     " @ " __FILE__ ":" + std::to_string(__LINE__)); \
        }                                                                     \
    } while (0)

#define CHECK_NEAR(a, b, tol)                                                 \
    do {                                                                      \
        if (std::fabs(double(a) - double(b)) > double(tol)) {                 \
            throw ::lqttest::Failure(std::string("CHECK_NEAR failed: " #a " ~= " #b) + \
                                     " @ " __FILE__ ":" + std::to_string(__LINE__)); \
        }                                                                     \
    } while (0)

#define CHECK_THROWS_AS(expr, ExcType)                                        \
    do {                                                                      \
        bool _threw = false;                                                  \
        try { (void)(expr); }                                                 \
        catch (const ExcType&) { _threw = true; }                            \
        catch (...) {                                                         \
            throw ::lqttest::Failure("CHECK_THROWS_AS wrong type: " #expr     \
                                     " @ " __FILE__ ":" + std::to_string(__LINE__)); \
        }                                                                     \
        if (!_threw) {                                                        \
            throw ::lqttest::Failure("CHECK_THROWS_AS did not throw: " #expr  \
                                     " @ " __FILE__ ":" + std::to_string(__LINE__)); \
        }                                                                     \
    } while (0)
